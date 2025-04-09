// This includes the precompiled header. Change this to whatever is relevant for your project.

#include "ImageLoader.h"
#include "IImageWrapperModule.h"
#include "IImageWrapper.h"
#include "Misc/FileHelper.h"
#include "RenderUtils.h"
#include "Engine/Texture2D.h"
#include "ModuleManager.h"
#include "Chuangshi.h"
#include "LogMacros.h"
#include "Paths.h"
#include "Async.h"
#include "PlatformFilemanager.h"

UTexture2D* UImageLoader::MiniMapTexture = nullptr;
UTexture2D* UImageLoader::BigMapTexture = nullptr;
UImageLoader::UImageLoader()
{
	//模块加载不允许在主线程之外
	ImageWrapperModule = &FModuleManager::LoadModuleChecked<IImageWrapperModule>(FName("ImageWrapper"));
	MapResourcePath = FString::Printf(TEXT("%s/%s"), *FPaths::ProjectDir(), TEXT("Resources/MiniMap"));
}
UImageLoader::~UImageLoader()
{
	ImageWrapperModule = nullptr;
}

UImageLoader* UImageLoader::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UImageLoader>();
}

void UImageLoader::LoadMiniMapTexture(const FString& ImageName, FImageLoadCompleted EventBack /*= nullptr*/)
{
	FString Path = FString::Printf(TEXT("%s/%s.jpg"), *MapResourcePath, *ImageName);
	LoadImageAsync(true, Path, EventBack);
}

void UImageLoader::LoadBigMapTexture(const FString& ImageName, FOnImageLoadCompleted LoadCompletedEvent)
{
	if (ImageName.Equals(BigMapImgName))
	{
		if (IsValid(UImageLoader::BigMapTexture))

		{
			LoadCompletedEvent.ExecuteIfBound(UImageLoader::BigMapTexture);
		}
	}
	else
	{
		BigMapImgName = ImageName;
		FString Path = FString::Printf(TEXT("%s/%s.jpg"), *MapResourcePath, *ImageName);
		LoadImageAsync(false, Path, FImageLoadCompleted::CreateLambda([&, LoadCompletedEvent]()
		{
			LoadCompletedEvent.ExecuteIfBound(UImageLoader::BigMapTexture);
		}));
	}
}

void UImageLoader::LoadImageAsync(bool IsMiniMap, const FString& ImagePath, FImageLoadCompleted EventBack /*= nullptr*/)
{
	LoadImageFromDiskAsync(IsMiniMap, ImagePath, [this, EventBack]()
	{

		// Notify listeners about the loaded texture on the game thread.
		AsyncTask(ENamedThreads::GameThread, [this, EventBack]() { EventBack.ExecuteIfBound(); });
	});
}

void UImageLoader::LoadImageFromDiskAsync(bool IsMiniMap, const FString& ImagePath, TFunction<void()> CompletionCallback)
{
	// Run the image loading function asynchronously through a lambda expression, capturing the ImagePath string by value.
	// Run it on the thread pool, so we can load multiple images simultaneously without interrupting other tasks.
	Async<void>(EAsyncExecution::ThreadPool, [=]() {LoadImageFromDisk(IsMiniMap, ImagePath); }, CompletionCallback);
}

void UImageLoader::LoadImageFromDisk(bool IsMiniMap, const FString& ImagePath)
{
	// Check if the file exists first
	if (!FPlatformFileManager::Get().GetPlatformFile().FileExists(*ImagePath))
	{
		UE_LOG(LogTemp, Warning, TEXT("File not found: %s"), *ImagePath);
		return;
	}

	// Load the compressed byte data from the file
	TArray<uint8> CompressedData;
	if (!FFileHelper::LoadFileToArray(CompressedData, *ImagePath))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to load file: %s"), *ImagePath);
		return;
	}

	// Detect the image type using the ImageWrapper module
	EImageFormat ImageFormat = ImageWrapperModule->DetectImageFormat(CompressedData.GetData(), CompressedData.Num());
	if (ImageFormat == EImageFormat::Invalid)
	{
		UE_LOG(LogTemp, Error, TEXT("Unrecognized image file format: %s"), *ImagePath);
		return;
	}

	// Create an image wrapper for the detected image format
	TSharedPtr<IImageWrapper> ImageWrapper = ImageWrapperModule->CreateImageWrapper(ImageFormat);
	if (!ImageWrapper.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to create image wrapper for file: %s"), *ImagePath);
		return;
	}

	// Decompress the image data
	const TArray<uint8>* RawData = nullptr;
	ImageWrapper->SetCompressed(CompressedData.GetData(), CompressedData.Num());
	ImageWrapper->GetRaw(ERGBFormat::BGRA, 8, RawData);
	if (RawData == nullptr)
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to decompress image file: %s"), *ImagePath);
		return;
	}

	//Update Resource
	int32 SizeX = ImageWrapper->GetWidth();
	int32 SizeY = ImageWrapper->GetHeight();

	FUpdateTextureRegion2D* Region = new FUpdateTextureRegion2D(0, 0, 0, 0, SizeX, SizeY);
	TArray<uint8>* TextureData = new TArray<uint8>(MoveTemp(*(TArray<uint8>*)(RawData)));
	// cleanup functions, gets executed on the render thread after UpdateTextureRegions
	TFunction<void(uint8*, const FUpdateTextureRegion2D*)> DataCleanupFunc = [this](uint8* InTextureData, const FUpdateTextureRegion2D* InRegions)
	{
		//this is executed later on the render thread, meanwhile TextureData might have changed
		delete InTextureData;
		delete InRegions;
	};
	// Update it on the render thread
	if (IsMiniMap)
	{
		if (IsValid(MiniMapTexture))
		{
			MiniMapTexture->RemoveFromRoot();
			MiniMapTexture->MarkPendingKill();
		}
		MiniMapTexture = UTexture2D::CreateTransient(SizeX, SizeY, PF_B8G8R8A8);
		MiniMapTexture->UpdateResource();
		MiniMapTexture->UpdateTextureRegions((int32)0, (uint32)1, Region, (uint32)(4 * SizeX), (uint32)4, (uint8*)(*TextureData).GetData(), DataCleanupFunc);
		MiniMapTexture->AddToRoot();
	}
	else
	{
		if (IsValid(BigMapTexture))
		{
			BigMapTexture->RemoveFromRoot();
			BigMapTexture->MarkPendingKill();
		}
		BigMapTexture = UTexture2D::CreateTransient(SizeX, SizeY, PF_B8G8R8A8);
		BigMapTexture->UpdateResource();
		BigMapTexture->UpdateTextureRegions((int32)0, (uint32)1, Region, (uint32)(4 * SizeX), (uint32)4, (uint8*)(*TextureData).GetData(), DataCleanupFunc);
		BigMapTexture->AddToRoot();
	}
}
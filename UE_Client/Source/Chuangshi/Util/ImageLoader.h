#pragma once
#include "PixelFormat.h"
#include "Future.h"
#include "ImageLoader.generated.h"

// Forward declarations
class UTexture2D;
class IImageWrapperModule;
class IImageWrapper;

/**
Declare a broadcast-style delegate type, which is used for the load completed event.
Dynamic multicast delegates are the only type of event delegates that Blueprint scripts can bind to.
*/
DECLARE_DELEGATE(FImageLoadCompleted);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnImageLoadCompleted, UTexture2D*, Texture);

/**
Utility class for asynchronously loading an image into a texture.
Allows Blueprint scripts to request asynchronous loading of an image and be notified when loading is complete.
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UImageLoader : public UObject
{
	GENERATED_BODY()

public:
	UImageLoader();
	~UImageLoader();
	
	static UImageLoader* GetInstance();
	void LoadMiniMapTexture(const FString& ImageName, FImageLoadCompleted EventBack = nullptr);
	UTexture2D* GetMiniMapTexture() { return MiniMapTexture; };

	UFUNCTION(BlueprintCallable, DisplayName = "LoadBigMapTexture", Category = "Tool|ImageLoader")
	void LoadBigMapTexture(const FString& ImageName, FOnImageLoadCompleted LoadCompletedEvent);

private:
	void LoadImageAsync(bool IsMiniMap, const FString& ImagePath, FImageLoadCompleted EventBack = nullptr);
	/**
	Loads an image file from disk into a texture on a worker thread. This will not block the calling thread.
	*/
	void LoadImageFromDiskAsync(bool IsMiniMap, const FString& ImagePath, TFunction<void()> CompletionCallback);

	/**
	Loads an image file from disk into a texture. This will block the calling thread until completed.
	*/
	void LoadImageFromDisk(bool IsMiniMap, const FString& ImagePath);

private:
	IImageWrapperModule* ImageWrapperModule;
	static UTexture2D* MiniMapTexture;
	static UTexture2D* BigMapTexture;
	FString MapResourcePath;
	FString BigMapImgName;
};

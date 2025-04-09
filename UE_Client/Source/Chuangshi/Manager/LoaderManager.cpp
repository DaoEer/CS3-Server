// Fill out your copyright notice in the Description page of Project Settings.


#include "LoaderManager.h"
#include "StoryManager.h"
#include "GameStatus.h"
#include "Entity/Role/CS3Role.h"
#include "Actor/Player/PlayerCharacter.h"
#include"Chuangshi.h"
#include "GameStatus.h"
#include "MediaPlayerManager.h"
#include "CustomTimerManager.h"


CONTROL_COMPILE_OPTIMIZE_START
#pragma region UBaseDetect

UBaseDetect::UBaseDetect()
{

}

void UBaseDetect::StartDetect(FSLoadCallBack SCallBack)
{
	OnDetect(SCallBack);
	if (TimeoutTime>0.0f)
	{
		TWeakObjectPtr<UBaseDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimeoutTimer, FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				UBaseDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->CProgress = 1.0f;
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseDetect OnDetect is TiemOut"));
			}
		}), TimeoutTime, false);
	}	
}

void UBaseDetect::OnDetect(FSLoadCallBack SCallBack)
{
	CProgress += 0.5f;
	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseDetect:: Finished"));
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<UBaseDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid())
			{
				UBaseDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->OnDetect(SCallBack);
			}
		}), 0.03f, false);
	}
}

void UBaseDetect::FinishDetect()
{
	CProgress = 0.0f;
	if (DetectTimer.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DetectTimer);
	}
	if (TimeoutTimer.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimeoutTimer);
	}
}

void UBaseDetect::BeginDestroy()
{
	Super::BeginDestroy();
}

void UAssetDetect::StartDetect(FSLoadCallBack SCallBack)
{
	ResetData();
	Super::StartDetect(SCallBack);
}

void UAssetDetect::OnDetect(FSLoadCallBack SCallBack)
{
	if (bIsLoadAssetFinished)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		return;
	}
	else
	{
		if (CProgress < (float(CurCount) + SDProgress) / float(Count))
		{
			CProgress += 0.5f;
		}
	}

	if (CProgress >= 1.0f)
	{
		if (!bIsLoadAssetFinished)
		{
			CProgress = 0.99f;
		}
	}
	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<UAssetDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid())
			{
				UAssetDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->SDProgress += 0.1f;
				if (ThisPtr->SDProgress >= 1.0f)
				{
					ThisPtr->SDProgress = 0.99f;
				}
				if (SCallBack.IsBound())
				{
					ThisPtr->OnDetect(SCallBack);
				}
			}

		}), 0.03f, false);
	}
}

void UAssetDetect::FinishDetect()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT(" UAssetDetect::FinishDetect() "));
	Super::FinishDetect();
	ResetData();
}

void UAssetDetect::LoadAssetFinished()
{
	++CurCount;
	SDProgress = 0.0f;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT(" UAssetDetect::LoadStoryFinished Count=%d  CurCount=%d "), Count, CurCount);
	if (CurCount == Count)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimeoutTimer);
		bIsLoadAssetFinished = true;
	}
}

void UAssetDetect::ResetData()
{
	CurCount = 0;
	Count = 0;
	SDProgress = 0.0f;
	bIsLoadAssetFinished = false;
}

void UStoryDetect::StartDetect(FSLoadCallBack SCallBack)
{
	ResetData();
	UGStoryManager* GStoryManager = UUECS3GameInstance::Instance->GStoryManager;
	
	if (GStoryManager)
	{
		FLoadStoryOverDelegate InLoadStoryOverDelegate;
		InLoadStoryOverDelegate.AddUObject(this, &UStoryDetect::LoadAssetFinished);
		Count = GStoryManager->PreLoadStoryAsset(InLoadStoryOverDelegate);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UStoryDetect::StartDetect***************************StoryCount=%d"), Count);
		///<有可能资源已加载好了
		if ((Count == CurCount && CurCount > 0) || Count == 0)
		{
			bIsLoadAssetFinished = true;
		}
		else
		{
			float Timeout = FMath::Max(Count * 2.0f, 5.0f);
			TWeakObjectPtr<UStoryDetect> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimeoutTimer, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					UStoryDetect* ThisPtr = DelayThisPtr.Get();
					if (!ThisPtr->bIsLoadAssetFinished)
					{
						ThisPtr->bIsLoadAssetFinished = true;
					}
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("UStoryDetect::PreLoadStoryAssetData is TiemOut"));
				}
			}), Timeout, false);
		}
	}
	else
	{
		bIsLoadAssetFinished = true;
	}
	OnDetect(SCallBack);
}

void UMediaDetect::StartDetect(FSLoadCallBack SCallBack)
{
	ResetData();
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;

	if (MediaPlayerManager)
	{
		FLoadMediaOverDelegate InLoadStoryOverDelegate;
		InLoadStoryOverDelegate.AddUObject(this, &UMediaDetect::LoadAssetFinished);
		Count = MediaPlayerManager->PreLoadMediaAsset(InLoadStoryOverDelegate);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaDetect::StartDetect***************************Count=%d"), Count);
		///<有可能资源已加载好了
		if ((Count == CurCount && CurCount > 0) || Count == 0)
		{
			bIsLoadAssetFinished = true;
		}
		else
		{
			TWeakObjectPtr<UMediaDetect> DelayThisPtr(this);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimeoutTimer, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					UMediaDetect* ThisPtr = DelayThisPtr.Get();
					if (!ThisPtr->bIsLoadAssetFinished)
					{
						ThisPtr->bIsLoadAssetFinished = true;
					}
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaDetect::PreLoadStoryAssetData is TiemOut"));
				}
			}), Count*2.0f, false);
		}
	}
	else
	{
		bIsLoadAssetFinished = true;
	}
	OnDetect(SCallBack);
}

void UWorldSceneDetect::StartDetect(FSLoadCallBack SCallBack)
{
	OnDetect(SCallBack);	
}

void UWorldSceneDetect::OnDetect(FSLoadCallBack SCallBack)
{
	CProgress += 0.2f;

	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
	{
		if (CProgress >= 1.0f)
		{
			CProgress = 0.99f;
		}
	}
	else
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UWorldSceneDetect::SceneDetect Finished"));
		return;
	}
	
	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UWorldSceneDetect::SceneDetect Finished"));
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<UWorldSceneDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid() && SCallBack.IsBound())
			{
				UWorldSceneDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->OnDetect(SCallBack);
			}

		}), 0.1f, false);
	}
}

void UWorldSceneDetect::FinishDetect()
{
	Super::FinishDetect();	
}

void ULoginSceneDetect::OnDetect(FSLoadCallBack SCallBack)
{
	CProgress += 0.3f;
	if (CProgress >= 1.0f)
	{
		if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport))
		{
			CProgress = 0.99f;
		}
	}
	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<ULoginSceneDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid())
			{
				ULoginSceneDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->OnDetect(SCallBack);
			}
		}), 0.1f, false);
	}
}

void UPlayerCharacterDetect::StartDetect(FSLoadCallBack SCallBack)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPlayerCharacterDetect::StartDetect"));
	OnDetect(SCallBack);
}

void UPlayerCharacterDetect::OnDetect(FSLoadCallBack SCallBack)
{
	CProgress += 0.2f;

	KBEngine::Entity *entity = UUECS3GameInstance::pKBEApp->Player();

	if (entity != nullptr)
	{
		CS3Entity* pEntity_Player = (CS3Entity*)(entity);
		if (pEntity_Player && pEntity_Player->IsPlayerRole())
		{
			CS3Role *role = (CS3Role *)entity;
			APlayerCharacter* SelfPlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			if (!IsValid(SelfPlayerCharacter) || !SelfPlayerCharacter->GetApperanceLoadingOver())
			{
				if (CProgress >= 1.0f)
				{
					CProgress = 0.99f;
				}
			}
			else if (SelfPlayerCharacter->GetApperanceLoadingOver())
			{
				FinishDetect();
				SCallBack.ExecuteIfBound(1.0f);
				SCallBack.Unbind();
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPlayerCharacterDetect::OnDetect Finished"));
				return;
			}
		}
	}

	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPlayerCharacterDetect::OnDetect Finished"));
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<UPlayerCharacterDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid())
			{
				UPlayerCharacterDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->OnDetect(SCallBack);
			}
		}), 0.03f, false);
	}
}

void UPlayerCharacterDetect::FinishDetect()
{
	Super::FinishDetect();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPlayerCharacterDetect::FinishDetect"));
}

void UGuisDetect::OnDetect(FSLoadCallBack SCallBack)
{
	Super::OnDetect(SCallBack);
}

void UConfigDetect::OnDetect(FSLoadCallBack SCallBack)
{
	Super::OnDetect(SCallBack);
}

void UParticleDetect::OnDetect(FSLoadCallBack SCallBack)
{
	Super::OnDetect(SCallBack);
}

void UPlayMediaDetect::OnDetect(FSLoadCallBack SCallBack)
{
	CProgress += 0.2f;
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;

	if (IsValid(MediaPlayerManager))
	{
		if (MediaPlayerManager->IsPlaying()&& !MediaPlayerManager->IsCanStopByMinimumTime() && MediaPlayerManager->IsStopInWorldOver())
		{
			if (CProgress >= 1.0f)
			{
				CProgress = 0.99f;
			}
		}
	}

	if (CProgress >= 1.0f)
	{
		FinishDetect();
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMediaPlayedDetect::OnDetect Finished"));
	}
	else
	{
		SCallBack.ExecuteIfBound(CProgress);
		TWeakObjectPtr<UPlayMediaDetect> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DetectTimer, FTimerDelegate::CreateLambda([DelayThisPtr, SCallBack]()
		{
			if (DelayThisPtr.IsValid())
			{
				UPlayMediaDetect* ThisPtr = DelayThisPtr.Get();
				ThisPtr->OnDetect(SCallBack);
			}
		}), 0.02f, false);
	}
}


void UPlayMediaDetect::FinishDetect()
{
	Super::FinishDetect();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UPlayMediaDetect::FinishDetect"));
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;

	if (IsValid(MediaPlayerManager)&& MediaPlayerManager->IsPlaying()&& MediaPlayerManager->IsStopInWorldOver())
	{
		MediaPlayerManager->Close(true);
	}
}
#pragma endregion

#pragma region UBaseLoader

UBaseLoader::UBaseLoader()
{
	//PrimaryComponentTick.bCanEverTick = false;
}

void UBaseLoader::Run(FTLoadCallBack TCallBack)
{

}

void UBaseLoader::Detect()
{
	if (LoadDetectorList.Num() > 0)
	{
		float SProgress = LoadProgressList.Pop();
		CurrLoadDetector = LoadDetectorList.Pop();
		CurrLoadDetector.Broadcast(FSLoadCallBack::CreateLambda([this, SProgress](float Progress)
		{
			TLoadCallBack.ExecuteIfBound(TotalProgress + Progress * SProgress);
			if (Progress >= 1.0f)
			{
				 TotalProgress += SProgress;
				if (LoadDetectorList.Num() > 0)
				{
					Detect();
				}
			}
		}));
	}
	else
	{
		TLoadCallBack.ExecuteIfBound(1.0f);
		TLoadCallBack.Unbind();
	}
}

void UBaseLoader::Cancel()
{
	if (LoadTimer.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(LoadTimer);
	}
	TLoadCallBack = FTLoadCallBack();
}

void UBaseLoader::BeginDestroy()
{
	Super::BeginDestroy();
}

#pragma endregion

#pragma region ULoginLoader

void ULoginLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(LoginSceneDetector))
	{
		LoginSceneDetector = NewObject<ULoginSceneDetect>();
	}
	LoadProgressList.Add(1.0f);
	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &ULoginLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void ULoginLoader::Detect()
{
	Super::Detect();
}

void ULoginLoader::Cancel()
{
	Super::Cancel();
}

void ULoginLoader::SceneDetect(FSLoadCallBack SCallBack)
{
	if (LoginSceneDetector)
	{
		LoginSceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}	
}

#pragma endregion

#pragma region UCampLoader

void UCampLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(LoginSceneDetector))
	{
		LoginSceneDetector = NewObject<ULoginSceneDetect>();
	}
	LoadProgressList.Add(1.0f);
	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &UCampLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void UCampLoader::Detect()
{
	Super::Detect();
}

void UCampLoader::Cancel()
{
	Super::Cancel();
}

void UCampLoader::SceneDetect(FSLoadCallBack SCallBack)
{
	if (LoginSceneDetector)
	{
		LoginSceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

#pragma endregion

#pragma region UCreatorLoader

void UCreatorLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(LoginSceneDetector))
	{
		LoginSceneDetector = NewObject<ULoginSceneDetect>();
	}
	LoadProgressList.Add(1.0f);
	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &UCreatorLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void UCreatorLoader::Detect()
{
	Super::Detect();
}

void UCreatorLoader::Cancel()
{
	Super::Cancel();
}

void UCreatorLoader::SceneDetect(FSLoadCallBack SCallBack)
{
	if (LoginSceneDetector)
	{
		LoginSceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

#pragma endregion

#pragma region USelectorLoader

void USelectorLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(LoginSceneDetector))
	{
		LoginSceneDetector = NewObject<ULoginSceneDetect>();
	}
	LoadProgressList.Add(1.0f);
	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &USelectorLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void USelectorLoader::Detect()
{
	Super::Detect();
}

void USelectorLoader::Cancel()
{
	Super::Cancel();
}

void USelectorLoader::SceneDetect(FSLoadCallBack SCallBack)
{
	if (LoginSceneDetector)
	{
		LoginSceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

#pragma endregion

#pragma region UWorldLoader

void UWorldLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(SceneDetector))
	{
		SceneDetector = NewObject<UWorldSceneDetect>();
	}
	
	if (!IsValid(PlayerCharacterDetector))
	{
		PlayerCharacterDetector = NewObject<UPlayerCharacterDetect>();
	}
#if WITH_EDITOR
	LoadProgressList.Add(0.4f);
	LoadProgressList.Add(0.6f);	
	FLoadDelegate PlayerCharacterDelegate;
	PlayerCharacterDelegate.AddUObject(this, &UWorldLoader::PlayerCharacterDetect);
	LoadDetectorList.Add(PlayerCharacterDelegate);
#else
	if (!IsValid(StoryDetector))
	{
		StoryDetector = NewObject<UStoryDetect>();
	}
	if (!IsValid(MediaDetector))
	{
		MediaDetector = NewObject<UMediaDetect>();
	}
	LoadProgressList.Add(0.2f);
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.6f);
	///注意下列代理的添加顺序，它是是先添加反而在后面开始监测
	FLoadDelegate PlayerCharacterDelegate;
	PlayerCharacterDelegate.AddUObject(this, &UWorldLoader::PlayerCharacterDetect);
	LoadDetectorList.Add(PlayerCharacterDelegate);
	FLoadDelegate MediaDelegate;
	MediaDelegate.AddUObject(this, &UWorldLoader::MediaDetect);
	LoadDetectorList.Add(MediaDelegate);
	FLoadDelegate StoryDelegate;
	StoryDelegate.AddUObject(this, &UWorldLoader::StoryDetect);
	LoadDetectorList.Add(StoryDelegate);
#endif	
	
	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &UWorldLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);	
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void UWorldLoader::Detect()
{
	Super::Detect();
}

void UWorldLoader::Cancel()
{
	Super::Cancel();
}

void UWorldLoader::ConfigDetect(FSLoadCallBack SCallBack)
{

}

void UWorldLoader::GuisDetect(FSLoadCallBack SCallBack)
{
	
}

void UWorldLoader::SceneDetect(FSLoadCallBack SCallBack)
{
	if (SceneDetector)
	{
		SceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UWorldLoader::StoryDetect(FSLoadCallBack SCallBack)
{		
	if (StoryDetector)
	{
		StoryDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UWorldLoader::MediaDetect(FSLoadCallBack SCallBack)
{
	if (MediaDetector)
	{
		MediaDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UWorldLoader::PlayerCharacterDetect(FSLoadCallBack SCallBack)
{
	if (PlayerCharacterDetector)
	{
		PlayerCharacterDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

#pragma endregion

#pragma region UTeleportLoader

void UTeleportLoader::Run(FTLoadCallBack TCallBack)
{
	if (!IsValid(SceneDetector))
	{
		SceneDetector = NewObject<UWorldSceneDetect>();
	}

	if (!IsValid(PlayerCharacterDetector))
	{
		PlayerCharacterDetector = NewObject<UPlayerCharacterDetect>();
	}
	if (!IsValid(PlayMediaDetector))
	{
		PlayMediaDetector = NewObject<UPlayMediaDetect>();
	}
	
#if WITH_EDITOR
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.3f);
	LoadProgressList.Add(0.6f);
	FLoadDelegate PlayMediaDelegate;
	PlayMediaDelegate.AddUObject(this, &UTeleportLoader::PlayMediaDetect);
	LoadDetectorList.Add(PlayMediaDelegate);
	FLoadDelegate PlayerCharacterDelegate;
	PlayerCharacterDelegate.AddUObject(this, &UTeleportLoader::PlayerCharacterDetect);
	LoadDetectorList.Add(PlayerCharacterDelegate);
#else
	if (!IsValid(StoryDetector))
	{
		StoryDetector = NewObject<UStoryDetect>();
	}
	if (!IsValid(MediaDetector))
	{
		MediaDetector = NewObject<UMediaDetect>();
	}
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.1f);
	LoadProgressList.Add(0.6f);
	///注意下列代理的添加顺序，它是是先添加反而在后面开始监测
	FLoadDelegate PlayMediaDelegate;
	PlayMediaDelegate.AddUObject(this, &UTeleportLoader::PlayMediaDetect);
	LoadDetectorList.Add(PlayMediaDelegate);
	FLoadDelegate PlayerCharacterDelegate;
	PlayerCharacterDelegate.AddUObject(this, &UTeleportLoader::PlayerCharacterDetect);
	LoadDetectorList.Add(PlayerCharacterDelegate);
	FLoadDelegate MediaDelegate;
	MediaDelegate.AddUObject(this, &UTeleportLoader::MediaDetect);
	LoadDetectorList.Add(MediaDelegate);
	FLoadDelegate StoryDelegate;
	StoryDelegate.AddUObject(this, &UTeleportLoader::StoryDetect);
	LoadDetectorList.Add(StoryDelegate);
#endif

	FLoadDelegate SceneDelegate;
	SceneDelegate.AddUObject(this, &UTeleportLoader::SceneDetect);
	LoadDetectorList.Add(SceneDelegate);
	TLoadCallBack = TCallBack;
	TotalProgress = 0.0f;
	Detect();
}

void UTeleportLoader::Detect()
{
	Super::Detect();
}

void UTeleportLoader::Cancel()
{
	Super::Cancel();
}

void UTeleportLoader::SceneDetect(FSLoadCallBack SCallBack)
{	
	if (SceneDetector)
	{
		SceneDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UTeleportLoader::StoryDetect(FSLoadCallBack SCallBack)
{	
	if (StoryDetector)
	{
		StoryDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UTeleportLoader::MediaDetect(FSLoadCallBack SCallBack)
{
	if (MediaDetector)
	{
		MediaDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UTeleportLoader::PlayerCharacterDetect(FSLoadCallBack SCallBack)
{
	if (PlayerCharacterDetector)
	{
		PlayerCharacterDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}

void UTeleportLoader::PlayMediaDetect(FSLoadCallBack SCallBack)
{
	if (PlayMediaDetector)
	{
		PlayMediaDetector->StartDetect(SCallBack);
	}
	else
	{
		SCallBack.ExecuteIfBound(1.0f);
		SCallBack.Unbind();
	}
}
#pragma endregion

#pragma region UGLoaderManager

UGLoaderManager::UGLoaderManager()
{
	
}

UGLoaderManager::~UGLoaderManager()
{
	
}
void  UGLoaderManager::PostInitProperties()
{
	LoginLoader = NewObject<ULoginLoader>();
	CampLoader = NewObject<UCampLoader>();
	CreatorLoader = NewObject<UCreatorLoader>();
	SelectorLoader = NewObject<USelectorLoader>();
	WorldLoader = NewObject<UWorldLoader>();
	TeleportLoader = NewObject<UTeleportLoader>();
	Super::PostInitProperties();
}


UGLoaderManager* UGLoaderManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UGLoaderManager *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GLoaderManager")));
}


void UGLoaderManager::LoadLoginSpace(FEndLoadCallBack EndCallBack)
{
	CurrLoader = LoginLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Login Space Run!"));
	LoginLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
			
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Login Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}

void UGLoaderManager::LoadCampSpace(FEndLoadCallBack EndCallBack)
{	
	CurrLoader = CampLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Camp Space Run!"));
	CampLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
			
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Camp Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}

void UGLoaderManager::LoadCreatorSpace(FEndLoadCallBack EndCallBack)
{	
	CurrLoader = CreatorLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Creator Space Run!"));
	CreatorLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
		
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Creator Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}

void UGLoaderManager::LoadSelectorSpace(FEndLoadCallBack EndCallBack)
{
	CurrLoader = SelectorLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Selector Space Run!"));
	SelectorLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
			
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Selector Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}

void UGLoaderManager::LoadWorldSpace(FEndLoadCallBack EndCallBack)
{
	CurrLoader = WorldLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading World Space Run!"));
	WorldLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading World Space Progress[%.3f]!"), Progress);
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
			
			UUECS3GameInstance::Instance->GameStatus->OnInWorldLoadingOver();
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading World Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}

void UGLoaderManager::LoadTeleportSpace(FEndLoadCallBack EndCallBack)
{	
	CurrLoader = TeleportLoader;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Teleport Space Run!"));
	TeleportLoader->Run(FTLoadCallBack::CreateLambda([this, EndCallBack](float Progress)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Teleport  Space Progress[%.3f]"), Progress);
		if (Progress >= 1.0f)
		{
			CurrLoader = nullptr;
			EndCallBack.ExecuteIfBound();
			
			UUECS3GameInstance::Instance->GameStatus->OnInWorldLoadingOver();
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Loading Teleport Space End!"));
			return;
		}
		OnProgressNotify(Progress);
	}));
}
CONTROL_COMPILE_OPTIMIZE_END

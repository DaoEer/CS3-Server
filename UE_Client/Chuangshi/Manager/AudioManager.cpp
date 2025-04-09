// Fill out your copyright notice in the Description page of Project Settings.


#include "AudioManager.h"
#include "AudioDevice.h"
#include "Util/CS3Debug.h"
#include "GameData/AudioData.h"
#include "GameData/VoiceData.h"
#include "GameData/SceneMusicData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Kismet/GameplayStatics.h"
#include "Components/CapsuleComponent.h"
#include "Components/SceneComponent.h"
#include "GameStatus.h"
#include "ResourceManager.h"
#include "LocalDataSaveManager.h"
#include "MapManager.h"
#include "CustomTimerManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CfgManager.h"
#include "Util/ConvertUtil.h"
#include"Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("InitAudioComp"), STAT_InitAudioComp, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("InitAudioData"), STAT_InitAudioData, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("CheckVoicePlay"), STAT_CheckVoicePlay, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("StopVoice"), STAT_StopVoice, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("PlaySceneAndEnvironmentMusic"), STAT_PlaySceneAndEnvironmentMusic, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("SetPausedVoice"), STAT_SetPausedVoice, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("PlaySceneMusicByAsset"), STAT_PlaySceneMusicByAsset, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("GetAudioAsset"), STAT_GetAudioAsset, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("GetSceneMusicAsset"), STAT_GetSceneMusicAsset, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("AsyncPlay3DSound"), STAT_AsyncPlay3DSound, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("StopAll3DSound"), STAT_StopAll3DSound, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("CreateAudioComponent"), STAT_CreateAudioComponent, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("CheckHideVoice"), STAT_CheckHideVoice, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("PlaySceneMusic"), STAT_PlaySceneMusic, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("LoopPlaySceneMusicByPlayerState"), STAT_LoopPlaySceneMusicByPlayerState, STATGROUP_AAudioManager);
DECLARE_CYCLE_STAT(TEXT("ClearAudioData"), STAT_ClearAudioData, STATGROUP_AAudioManager);

AAudioManager::AAudioManager()
{
	PrimaryActorTick.bCanEverTick = true;
	// 初始化
	InitAudioComp();
	InitAudioData();
}

void AAudioManager::Destroyed()
{
	Super::Destroyed();
	if (EmptySound)
	{
		EmptySound = nullptr;
	}
	VoiceDelayList.Empty();
	StoryVoiceList.Empty();
	BgMusicRandomArray.Empty();
	FightMusicRandomArray.Empty();
	HideVoiceTypes.Empty();
	DefualtHideVoiceTypes.Empty();
}

AAudioManager* AAudioManager::GetInstance()
{
	cs3_checkNoReentry();

	return UGolbalBPFunctionLibrary::SpawnActor<AAudioManager>(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_AudioManager")));
}

void AAudioManager::BeginPlay()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}
	Super::BeginPlay();
}

void AAudioManager::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	if (VoiceComp->OnVirtualAudioFinished.IsBound())
	{
		VoiceComp->OnVirtualAudioFinished.Clear();
	}
	if (ClientVoiceComp->OnVirtualAudioFinished.IsBound())
	{
		ClientVoiceComp->OnVirtualAudioFinished.Clear();
	}
	if (BgMusicComp->OnVirtualAudioFinishedNative.IsBound())
	{
		BgMusicComp->OnVirtualAudioFinishedNative.Clear();
	}
	if (FightMusicComp->OnVirtualAudioFinishedNative.IsBound())
	{
		FightMusicComp->OnVirtualAudioFinishedNative.Clear();
	}
	if (BgEffectComp->OnVirtualAudioFinished.IsBound())
	{
		BgEffectComp->OnVirtualAudioFinished.Clear();
	}
	if (PreviewSoundComp->OnVirtualAudioFinished.IsBound())
	{
		PreviewSoundComp->OnVirtualAudioFinished.Clear();
	}
	if (EnvironmentSoundComp->OnVirtualAudioFinished.IsBound())
	{
		EnvironmentSoundComp->OnVirtualAudioFinished.Clear();
	}
}

void AAudioManager::BeginDestroy()
{
	Super::BeginDestroy();
}

void AAudioManager::InitAudioComp()
{
	SCOPE_CYCLE_COUNTER(STAT_InitAudioComp);
	// 初始化音频组件
	VoiceComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("VoiceComp"));
	RootComponent = VoiceComp;
	ClientVoiceComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("ClientVoiceComp"));
	ClientVoiceComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	BgMusicComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("BgMusicComp"));
	BgMusicComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	FightMusicComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("FightMusicComp"));
	FightMusicComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	BgEffectComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("BgEffectComp"));
	BgEffectComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	PreviewSoundComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("PreviewSoundComp"));
	PreviewSoundComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	EnvironmentSoundComp = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("EnvironmentSoundComp"));
	EnvironmentSoundComp->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
	SkillEffectAudioComponent.Empty();
	Audio3DComponent.Empty();
}

void AAudioManager::InitAudioData()
{
	SCOPE_CYCLE_COUNTER(STAT_InitAudioData);
	// 初始化基础数据
	if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr))
	{
		bEnableAudioPlay = UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->GetEnableAudioSystem();
	}

	EmptySound = LoadObject<USoundBase>(nullptr, TEXT("/Game/Medias/Sounds/ProgrammerUse/EmptySound.EmptySound"));
	DefualtHideVoiceTypes.Reset();
	HideVoiceTypes.Reset();

	const FSoftObjectPath DefaultSoundClassName = GetDefault<UAudioSettings>()->DefaultSoundClassName;
	// 这里一定要有设置主声音类,不然就运行崩溃
	checkf(DefaultSoundClassName.IsValid(), TEXT("AAudioManager::InitAudioData() Error!!!!!  DefaultSoundClassName == Null"));
	MasterSoundClass = LoadObject<USoundClass>(nullptr, *DefaultSoundClassName.ToString());
}

bool AAudioManager::CheckPlayVoice(CSTORY_VOICE_TYPE VoiceType)
{
	if (CheckHideVoice(VoiceType)|| !bEnableAudioPlay)return false;
	return true;
}

void AAudioManager::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	CheckSceneMusic();
}

bool AAudioManager::CheckVoicePlay(FVOICE_DATA VoiceData)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckVoicePlay);
	uint8 InPriority = uint8(VoiceData.Priority);
	if (InPriority < VoicePriority)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::CheckVoicePlay -> AudioId[%s] priority is lower !"), *(VoiceData.AudioId));
		return false;
	}
	if (InPriority == VoicePriority)
	{
		VoiceDelayList.Add(VoiceData);
		if (!VoiceComp->OnVirtualAudioFinished.IsBound())
		{
			LoopPlayVoice();
		}
	}
	else
	{
		StopVoice();
		VoiceDelayList.Add(VoiceData);
		VoicePriority = InPriority;
		if (VoiceData.Delay > 0.1f)
		{
			// 不建议延迟加复杂逻辑(默认第一个才会有延迟效果)
			DelayPlayVoice(VoiceData.Delay);
		}
		else
		{
			LoopPlayVoice();
		}
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::CheckVoicePlay -> VoiceDelayList Num[%d]"), VoiceDelayList.Num());
	return true;
}

void AAudioManager::PlayVoice(const FString& AudioId)
{
	if (USoundBase* SoundAsset = GetAudioAsset(AudioId))
	{
		USoundWave* SoundWave = Cast<USoundWave>(SoundAsset);
		if (SoundWave)
		{
			SoundWave->bVirtualizeWhenSilent = true;
		}
		SoundAsset->bHasVirtualizeWhenSilent = true;
		VoiceComp->SetVolumeMultiplier(GetVoiceVol());
		VoiceComp->Sound = SoundAsset;
		VoiceComp->Play();
	}
}

void AAudioManager::BreakVoice()
{
	if (VoiceDelayList.Num() > 0)
	{
		VoiceComp->Stop();
	}
	else
	{
		StopVoice();
	}
}

void AAudioManager::StopVoice()
{
	SCOPE_CYCLE_COUNTER(STAT_StopVoice);
	if (VoiceComp->Sound)
	{
		VoicePriority = 0U;
		VoiceDelayList.Empty();
		StoryVoiceList.Empty();
		VoiceComp->Stop();
		VoiceComp->Sound = nullptr;
		LastVoiceId = TEXT("");
		if (VoiceComp->OnVirtualAudioFinished.IsBound())
			VoiceComp->OnVirtualAudioFinished.Clear();

		URolePerformanceInterface * Interface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
		if (Interface)
		{
			Interface->SetCurVoiceIds(TEXT(""));
		}
		BP_StopVoice();
	}
}

void AAudioManager::DelayPlayVoice(float Delay)
{
	if (IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayTimerHandle, this, &AAudioManager::LoopPlayVoice, Delay);
	}
}

void AAudioManager::SetLastVoiceId(FString lastVoiceId)
{
	LastVoiceId = lastVoiceId;
}

void AAudioManager::PausedVoice(bool bPause)
{
	if (bPause)
	{
		BreakVoice();
	}
	else
	{
		if (VoiceComp->IsPlaying())return;
		
		if (VoiceDelayList.Num() > 0)
		{
			LoopPlayVoice();
		}
	}
}

void AAudioManager::ClientVoicePlay(const FString& AudioId, FCClientVoiceComplete ClientVoiceCreate)
{
	ClientVoiceStop();
	if (!CheckPlayVoice(CSTORY_VOICE_TYPE::CLIENTVOICE))return;
	if (USoundBase* SoundAsset = GetAudioAsset(AudioId))
	{
		USoundWave* SoundWave = Cast<USoundWave>(SoundAsset);
		if (SoundWave)
		{
			SoundWave->bVirtualizeWhenSilent = true;
		}
		SoundAsset->bHasVirtualizeWhenSilent = true;
		ClientVoiceId = AudioId;
		ClientVoiceComp->SetVolumeMultiplier(GetVoiceVol());
		ClientVoiceComp->SetSound(SoundAsset);
		ClientVoiceComp->Play();
		OnCClientVoiceComplete = ClientVoiceCreate;
		if (!ClientVoiceComp->OnVirtualAudioFinishedNative.IsBoundToObject(this))
		{
			ClientVoiceComp->OnVirtualAudioFinishedNative.AddUObject(this, &AAudioManager::OnClientVoiceFinished);
		}		
	}
}

void AAudioManager::ClientVoiceStop()
{
	if (ClientVoiceComp->IsPlaying())
	{
		ClientVoiceComp->Stop();
	}
}

void AAudioManager::OnClientVoiceFinished(UAudioComponent * AudioComponent)
{
	if (ClientVoiceId.Compare(TEXT("")))
	{
		///<避免在OnCClientVoiceComplete回调中赋值后又被置空
		FString FinishedVoiceId = ClientVoiceId;
		ClientVoiceId = TEXT("");		
		OnCClientVoiceComplete.ExecuteIfBound(FinishedVoiceId);
		if (!ClientVoiceId.Compare(TEXT("")))
		{
			OnCClientVoiceComplete = nullptr;
			ClientVoiceComp->Sound = nullptr;
		}		
	}
}

FString AAudioManager::GetVoiceContentText(const FString& VoiceId) const
{
	FString ContentText = TEXT("");
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* VoiceConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_VOICE);
	if (IsValid(VoiceConfig))
	{	
		FVOICE_DATA* VoiceData = (FVOICE_DATA*)VoiceConfig->GetRow<FVOICE_DATA>(VoiceId);
		if (VoiceData)
		{
			ContentText = VoiceData->Content;
		}
	}
	return ContentText;
}

void AAudioManager::PlaySceneAndEnvironmentMusic()
{
	SCOPE_CYCLE_COUNTER(STAT_PlaySceneAndEnvironmentMusic);
	ResetSceneMusicData();
	UGameStatus* GameState = UUECS3GameInstance::Instance->GameStatus;
	if (GameState && (GameState->IsCurrStatus(EGameStatus::InWorld)|| GameState->IsCurrStatus(EGameStatus::Teleport)))
	{
		LoopPlaySceneMusicByPlayerState(true, true, true);
	}
	else
	{
		LoopPlaySceneMusicByPlayerState(true, true);
	}
	
	PlayEnvironmentSound();
}

void AAudioManager::SetPausedVoice(TArray<FString> CurPauseTypes, TArray<FString> CurHideTypes, bool bPause /*= true*/, bool bIsHideVoiceType /*= true*/)
{
	SCOPE_CYCLE_COUNTER(STAT_SetPausedVoice);
	/** 0.暂停语音类型  1.暂停战斗音乐
	2.暂停背景音乐		3.纯客户端语音
	4.3D语音			5.环境音效 例0|1|2|4|5 */
	if (bPause)
	{
		// 中断所有语音
		StopVoice();
	}

	if (bIsHideVoiceType)
	{
		SetHideVoice(CurHideTypes);
	}
	else
	{
		SetDefualtHideVoiceTypes(CurHideTypes);
	}

	///<重新播放战斗音乐或背景音乐根据玩家战斗状态播放
	if ((CurPauseTypes.Contains(TEXT("1")) || CurPauseTypes.Contains(TEXT("2"))) && !bPause)
	{
		LoopPlaySceneMusicByPlayerState(false, !bPause, true);
		if (CurPauseTypes.Contains(TEXT("1")))
		{
			CurPauseTypes.Remove(TEXT("1"));
		}
		if (CurPauseTypes.Contains(TEXT("2")))
		{
			CurPauseTypes.Remove(TEXT("2"));
		}
	}

	for (auto& Elem : CurPauseTypes)
	{
		int32 HideNum = FCString::Atoi(*Elem);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::SetPausedVoice -> HideType[%d]~"), HideNum);
		switch (HideNum)
		{
		case 0: PausedVoice(bPause); break;
		case 1:
		{
			LoopPlaySceneMusicByPlayerState(false, !bPause);
			break;
		}
		case 2:
		{
			LoopPlaySceneMusicByPlayerState(true, !bPause);
			break;
		}
		case 3:
		{
			if (bPause)
			{
				ClientVoiceStop();
			}
			break;
		}
		case 4:
		{
			PausedAll3DSound(bPause);
			break;
		}
		case 5:
		{
			PausedEnvironment(bPause);
			break;
		}
		case 6:
		{
			PausedWeather(bPause);
			break;
		}
		default: CS3_Warning(TEXT("AAudioManager::SetPausedVoice ->  HideNum[%s] is not found~"), *Elem); break;
		}
	}
}

void AAudioManager::RandomSceneMusicPlayArray(bool IsBgMusic, int MaxRandomNum)
{
	// 隨機播放順序
	TArray<int32> RandomArray;
	while (RandomArray.Num() < MaxRandomNum)
	{
		int32 Index = FMath::RandHelper(MaxRandomNum);
		if (!RandomArray.Contains(Index))
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::RandomSceneMusicPlayArray -> Index[%d]"), Index);
			RandomArray.AddUnique(Index);
		}
	}
	
	if (IsBgMusic)
		BgMusicRandomArray = RandomArray;
	else
		FightMusicRandomArray = RandomArray;
}

void AAudioManager::PlaySceneMusicByAsset(bool IsPlayBgMusic, USoundBase* SoundAsset, bool IsFindPlayList)
{
	SCOPE_CYCLE_COUNTER(STAT_PlaySceneMusicByAsset);
	if (!IsValid(SoundAsset))
		return;

	float FadeInTime = BgMusicFadeTimer;
	///<配置表中不是数组的情况下，背景音乐和战斗音乐一样不用切换音乐
	if (BgMusicComp->IsPlaying() && BgMusicComp->Sound && !IsFindPlayList)
	{
		FadeInTime += BgMusicFadeTimer;
		if (BgMusicComp->Sound == SoundAsset && CheckPlayVoice(CSTORY_VOICE_TYPE::FIGHTNUSIC))return;
	}
	else if (FightMusicComp->IsPlaying() && FightMusicComp->Sound && !IsFindPlayList)
	{
		FadeInTime += FightMusicFadeTimer;
		if (FightMusicComp->Sound == SoundAsset && CheckPlayVoice(CSTORY_VOICE_TYPE::BGMUSIC))return;
	}
	StopSceneMusic(!IsPlayBgMusic);
	if (IsPlayBgMusic)
	{
		if (!CheckPlayVoice(CSTORY_VOICE_TYPE::BGMUSIC))return;

		if (SoundAsset)
		{
			if (IsValid(Cast<USoundWave>(SoundAsset)))
			{
				if (!IsFindPlayList)
				{
					Cast<USoundWave>(SoundAsset)->bLooping = true;
				}
				else
				{
					Cast<USoundWave>(SoundAsset)->bLooping = false;
					if (CurrentBgMusicIndex < (BgMusicRandomArray.Num() - 1))
					{
						++CurrentBgMusicIndex;
					}
					else
					{
						CurrentBgMusicIndex = 0;
					}
				}
			}
			USoundWave* SoundWave = Cast<USoundWave>(SoundAsset);
			if (SoundWave)
			{
				SoundWave->bVirtualizeWhenSilent = true;
			}
			SoundAsset->bHasVirtualizeWhenSilent = true;
			BgMusicComp->Sound = SoundAsset;
			BgMusicComp->VolumeMultiplier = GetBgVol();
			BgMusicComp->FadeIn(FadeInTime);
			BgMusicComp->OnVirtualAudioFinishedNative.AddUObject(this, &AAudioManager::OnSceneAudioFinishedNative);
		}
	}
	else
	{
		if (!CheckPlayVoice(CSTORY_VOICE_TYPE::FIGHTNUSIC))return;

		// 开始播放战斗音乐
		if (IsValid(SoundAsset))
		{
			if (IsValid(Cast<USoundWave>(SoundAsset)))
			{
				if (!IsFindPlayList)
				{
					Cast<USoundWave>(SoundAsset)->bLooping = true;
				}
				else
				{
					Cast<USoundWave>(SoundAsset)->bLooping = false;

					if (CurrentFightMusicIndex < (FightMusicRandomArray.Num() - 1))
					{
						++CurrentFightMusicIndex;
					}
					else
					{
						CurrentFightMusicIndex = 0;
					}
				}
			}
			USoundWave* SoundWave = Cast<USoundWave>(SoundAsset);
			if (SoundWave)
			{
				SoundWave->bVirtualizeWhenSilent = true;
			}
			SoundAsset->bHasVirtualizeWhenSilent = true;
			FightMusicComp->Sound = SoundAsset;
			FightMusicComp->VolumeMultiplier = GetBgVol();
			FightMusicComp->FadeIn(FadeInTime);
			FightMusicComp->OnVirtualAudioFinishedNative.AddUObject(this, &AAudioManager::OnSceneAudioFinishedNative);
		}
	}
}

void AAudioManager::ResetSceneMusicData()
{
	bBgMusicRandomFinished = false;
	bFightMusicRandomFinished = false;
	CurrentBgMusicIndex = 0;
	CurrentFightMusicIndex = 0;
	BgMusicRandomArray.Reset();
	FightMusicRandomArray.Reset();
	bIsPlaySceneMusic = false;
	bIsPlayFightMusic = false;
	bIsStopSceneMusic = false;
	bIsStopFightMusic = false;
}

void AAudioManager::CheckSceneMusic()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (bIsStopSceneMusic)
		{
			bIsStopSceneMusic = false;
			StopSceneMusic(true);
		}
		if (bIsStopFightMusic)
		{
			bIsStopFightMusic = false;
			StopSceneMusic(false);
		}
		if (bIsPlaySceneMusic)
		{
			bIsPlaySceneMusic = false;
			PlaySceneMusic(true);
		}
		if (bIsPlayFightMusic)
		{
			bIsPlayFightMusic = false;
			PlaySceneMusic(false);
		}
	}
}

USoundBase* AAudioManager::GetAudioAsset(const FString& AudioId, bool IsAsync, FStreamableDelegate DelegateToCall) const
{
	SCOPE_CYCLE_COUNTER(STAT_GetAudioAsset);
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FAUDIO_DATA* AudioData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_AUDIO)->GetRow<FAUDIO_DATA>(AudioId);
	USoundBase* soundAsset = nullptr;
	if (!AudioData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::GetAudioAsset : AudioData!"));
		soundAsset = EmptySound;
		return soundAsset;
	}
	int32 MaxAudioNum = AudioData->AudioAsset.Num();

	FAUDIO_DATA* NewData = const_cast<FAUDIO_DATA*>(AudioData);
	if (0 != MaxAudioNum)
	{
		TSoftObjectPtr<USoundBase> SoundAssetPtr;
		if (1 == MaxAudioNum)
		{
			SoundAssetPtr = NewData->AudioAsset[0];
		}
		else
		{
			//策划有配2个数据的，由于没性别，配2个的暂时默认播放男性语音
			int32 gender = UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("gender"));
			if (gender == 1)
			{
				SoundAssetPtr = NewData->AudioAsset[0];
			}
			else if (gender == 2)
			{
				SoundAssetPtr = NewData->AudioAsset[1];
			}
#if WITH_EDITOR
			else if (gender == 0)
			{
				//不进入游戏时（如半身像配置关卡），没有性别数据，默认播放第一个语音
				SoundAssetPtr = NewData->AudioAsset[0];
			}
#endif
			else
			{
				CS3_Warning(TEXT("AAudioManager::GetSoundAsset -> INFO: 当前角色性别参数不符合预设[%d]"), gender);
			}
		}

		if (SoundAssetPtr.ToSoftObjectPath().IsValid())
		{
			if (!IsValid(SoundAssetPtr.Get()))
			{
				if (IsAsync)
				{
					UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, SoundAssetPtr.ToSoftObjectPath(), DelegateToCall, RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_MEDIA);
				}
				else
				{
					soundAsset = (USoundBase*)UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(SoundAssetPtr);
				}
			}
			else
			{
				soundAsset = SoundAssetPtr.Get();
				if (DelegateToCall.IsBound())
				{
					DelegateToCall.Execute();
				}
			}
		}


	}
	if (!soundAsset && !IsAsync)
	{
		soundAsset = EmptySound;
		CS3_Warning(TEXT("AAudioManager::GetSoundAsset -> AudioId[%d] asset is not found!"), *AudioId);
	}
	return soundAsset;
}

void AAudioManager::AsynLoadAudioAsset(const FString& AudioId, FAsynLoadAudioAssetComplete OnComplete)
{
	GetAudioAsset(AudioId, true, FStreamableDelegate::CreateLambda([OnComplete]()
	{
		OnComplete.ExecuteIfBound();
	}));
}

void AAudioManager::PreLoadAudioAsset(const FString& AudioId)
{
	AsynLoadAudioAsset(AudioId, FAsynLoadAudioAssetComplete());
}

USoundBase* AAudioManager::GetEnvironmentMusicAsset(const FString& SpaceId)
{
	if (SpaceId.IsEmpty())return nullptr;

	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FSCENEMUSIC_DATA* SceneMusicData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SCENE_MUSIC)->GetRow<FSCENEMUSIC_DATA>(SpaceId);

	FString newSpaceId = SpaceId;
	UMapManager* MapManager = UUECS3GameInstance::Instance->MapManager;
	bool isInPlane = MapManager->IsPlayerInPlane();
	if (SceneMusicData != nullptr)
	{
		if (isInPlane)
		{
			newSpaceId = MapManager->GetRelatedMapScriptID(SpaceId);
		}
		const FSCENEMUSIC_DATA* NewSceneMusicData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SCENE_MUSIC)->GetRow<FSCENEMUSIC_DATA>(newSpaceId);
		if (NewSceneMusicData == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::GetEnvironmentMusicAsset : NewSceneMusicData!"));
			return nullptr;
		}
		if ((*NewSceneMusicData).EnvironmentMusic.ToSoftObjectPath().IsValid())
		{
			if (IsValid((*NewSceneMusicData).EnvironmentMusic.Get()))
			{
				return (*NewSceneMusicData).EnvironmentMusic.Get();
			}
			else
			{
				UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad((*NewSceneMusicData).EnvironmentMusic.ToSoftObjectPath());
				return (*NewSceneMusicData).EnvironmentMusic.Get();
			}
		}
	}
	CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::GetEnvironmentMusicAsset : SceneMusicData!"));
	return nullptr;
}

void AAudioManager::PausedEnvironment(bool bIsPaused /*= false*/)
{
	if (IsValid(EnvironmentSoundComp))
	{
		if (EnvironmentSoundComp->IsPlaying() && bIsPaused)
		{
			EnvironmentSoundComp->SetPaused(bIsPaused);
		}
		if (!bIsPaused && IsValid(EnvironmentSoundComp->Sound))
		{
			EnvironmentSoundComp->SetPaused(bIsPaused);
		}
	}
}

void AAudioManager::SetEnvironmentMusicVol(float Vol)
{
	Vol = 0.2f*Vol;///<环境音效最大为0.2
	if (Vol < 0.00011f)
	{
		if (IsValid(EnvironmentSoundComp))
		{
			EnvironmentSoundComp->SetVolumeMultiplier(0.00011f);
		}
	}
	else
	{
		if (IsValid(EnvironmentSoundComp))
		{
			EnvironmentSoundComp->SetVolumeMultiplier(Vol);
		}
	}
}

const FString AAudioManager::GetCurSpaceId()
{
	FString SpaceId = TEXT("");
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GameStatus))
	{
		EGameStatus CurStatus = UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
		switch (CurStatus)
		{
		case EGameStatus::Login:
			SpaceId = TEXT("L_Login");
			break;
		case EGameStatus::CreateRole:
			SpaceId = TEXT("L_Login_C");
			break;
		case EGameStatus::SelectRole:
			SpaceId = TEXT("L_Login_S");
			break;
		case EGameStatus::InWorld:
			SpaceId = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
			break;
		case EGameStatus::SelectCamp:
		case EGameStatus::Personalize:
		case EGameStatus::Logoff:
		case EGameStatus::Teleport:
			SpaceId = TEXT("");
			break;
		default:
			SpaceId = TEXT("");
			break;
		}
	}
	return SpaceId;
}

void AAudioManager::AnalysisVoiceData(const FString& Id)
{
	if (!bEnableAudioPlay)
	{
		CS3_Warning(TEXT("AAudioManager::AnalysisVoiceData -> bEnableAudioPlay false !~"));
		return;
	}
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* VoiceConfig = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_VOICE);
	bool bIsFindId = false;
	if (IsValid(VoiceConfig))
	{
		FVOICE_DATA* VoiceData = (FVOICE_DATA*)VoiceConfig->GetRow<FVOICE_DATA>(Id);
		if (VoiceData)
		{
			FVOICE_DATA VoiceDataInfo = *VoiceData;
			if (CheckVoicePlay(VoiceDataInfo))
			{
				bIsFindId = true;
				// TODO: 有效语音已加入播放链表
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::AnalysisVoiceData -> TODO: The VoiceData is add to play List, Id[%s], Content[%s]~"), *Id, *VoiceData->Content);
			}
		}
	}
	if (!bIsFindId)
	{
		CS3_Warning(TEXT("AAudioManager::AnalysisVoiceData -> VoiceConfig data has no Id[%s] !~"), *Id);
	}
}

TSoftObjectPtr<USoundBase> AAudioManager::GetSceneMusicAsset(bool IsBgMusic, bool& IsFindPlayList)
{
	SCOPE_CYCLE_COUNTER(STAT_GetSceneMusicAsset);
	const FString SpaceId = GetCurSpaceId();
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FSCENEMUSIC_DATA* SceneMusicData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SCENE_MUSIC)->GetRow<FSCENEMUSIC_DATA>(SpaceId);

	FString newSpaceId = SpaceId;
	UMapManager* MapManager = UUECS3GameInstance::Instance->MapManager;
	bool isInPlane = MapManager->IsPlayerInPlane();
	FSCENEMUSIC_DATA finalSceneMusicData;
	if (!SceneMusicData)
	{
		if (isInPlane)
		{
			newSpaceId = MapManager->GetRelatedMapScriptID(SpaceId);
			const FSCENEMUSIC_DATA* NewSceneMusicData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_SCENE_MUSIC)->GetRow<FSCENEMUSIC_DATA>(newSpaceId);
			if (!NewSceneMusicData)
			{
				CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::GetSceneMusicAsset : NewSceneMusicData!"));
				return nullptr;
			}
			else
			{
				finalSceneMusicData = *NewSceneMusicData;
			}
		}
		else
		{
			CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::GetSceneMusicAsset : NewSceneMusicData!"));
			return nullptr;
		}
	}
	else
	{
		finalSceneMusicData = *SceneMusicData;
	}

	TSoftObjectPtr<USoundBase> soundAssetPtr;
	if (IsBgMusic)
	{
		int32 MaxBgMusicNum = finalSceneMusicData.BgMusicList.Num();
		if (!bBgMusicRandomFinished)
		{
			bBgMusicRandomFinished = true;
			RandomSceneMusicPlayArray(IsBgMusic, MaxBgMusicNum);
		}
		if (0 == MaxBgMusicNum)
		{
			soundAssetPtr = finalSceneMusicData.DefaultBgMusic;
		}
		else
		{
			IsFindPlayList = true;
			soundAssetPtr = finalSceneMusicData.BgMusicList[BgMusicRandomArray[CurrentBgMusicIndex]];			
		}
	}
	else
	{
		int32 MaxFightMusicNum = finalSceneMusicData.FightMusicList.Num();
		if (!bFightMusicRandomFinished)
		{
			bFightMusicRandomFinished = true;
			RandomSceneMusicPlayArray(IsBgMusic, MaxFightMusicNum);
		}
		CS3_Warning(TEXT("AAudioManager::GetSceneMusicAsset -> FightMusicList[%d], FightMusicRandomArray[%d]"), MaxFightMusicNum, FightMusicRandomArray.Num());
		if (0 == MaxFightMusicNum)
		{
			soundAssetPtr = finalSceneMusicData.DefaultFightMusic;
		}
		else
		{
			IsFindPlayList = true;
			soundAssetPtr = finalSceneMusicData.FightMusicList[FightMusicRandomArray[CurrentFightMusicIndex]];
		}
	}
	return soundAssetPtr;
}

UCS3AudioComponent* AAudioManager::Play3DSound(AActor* TargetActor, const FString& AudioId, FVector Postion/*= FVector::ZeroVector*/, EAUDIOCOMPTYLE AudioCompType/*=EAUDIOCOMPTYLE::NONE*/, bool bIsLoop /*= false*/, USceneComponent* AttachComp /* = nullptr*/)
{
	CS3_Log(TEXT("AAudioManager::Play3DSound AudioId[%s],"), *AudioId);
	if (USoundBase* SoundAsset = GetAudioAsset(AudioId))
	{
		return Play3DSoundByAsset(TargetActor, SoundAsset, Postion, AudioCompType);
	}
	return nullptr;
}

UCS3AudioComponent* AAudioManager::AsyncPlay3DSound(AActor* TargetActor, const FString& AudioId, FVector Postion /*= FVector::ZeroVector*/, EAUDIOCOMPTYLE AudioCompType /*= EAUDIOCOMPTYLE::NONE*/, bool bIsLoop /*= false*/, USceneComponent* AttachComp /*= nullptr*/)
{
	CS3_Log(TEXT("AAudioManager::AsyncPlay3DSound AudioId[%s]"), *AudioId);
	SCOPE_CYCLE_COUNTER(STAT_AsyncPlay3DSound);
	if (!CheckPlayVoice(CSTORY_VOICE_TYPE::SOUND3D))return nullptr;
	UCS3AudioComponent* NewAudioComponent = CreateAudioComponent(TargetActor, Postion, AttachComp);

	float PlayTime = TargetActor->GetWorld()->TimeSeconds;

	TWeakObjectPtr<AAudioManager> AudioManagerPtr(this);
	TWeakObjectPtr<AActor> DelayTargetActorPtr(TargetActor);
	TWeakObjectPtr<UCS3AudioComponent> DelayNewAudioComponentPtr(NewAudioComponent);
	GetAudioAsset(AudioId, true, FStreamableDelegate::CreateLambda([AudioManagerPtr,PlayTime, DelayTargetActorPtr, DelayNewAudioComponentPtr, AudioId, bIsLoop, AudioCompType]()
	{		
		if (DelayNewAudioComponentPtr.IsValid() && DelayTargetActorPtr.IsValid() && AudioManagerPtr.IsValid())
		{
			AAudioManager*AudioManager = AudioManagerPtr.Get();
			USoundBase* SoundAsset = AudioManager->GetAudioAsset(AudioId);
			if (!IsValid(SoundAsset))
			{
				CS3_Warning(TEXT("-->Null Pointer error:AAudioManager::AsyncPlay3DSound : SoundAsset!"));
				return;
			}
			
			AActor* DelayTargetActor = DelayTargetActorPtr.Get();
			UCS3AudioComponent* DelayNewAudioComponent = DelayNewAudioComponentPtr.Get();
			float NowTime = DelayTargetActor->GetWorld()->TimeSeconds;
			float PastTime = NowTime - PlayTime;
			if (bIsLoop || PastTime < SoundAsset->GetDuration())
			{
				AudioManager->SetAudioComponent_AudioAsset(DelayTargetActor,DelayNewAudioComponent, bIsLoop, PastTime, SoundAsset, AudioCompType);
			}
			else
			{
				AudioManager->On3DAudioFinishedNative(DelayNewAudioComponent);
			}
		}
	}));

	return NewAudioComponent;
}

UCS3AudioComponent* AAudioManager::Play3DSoundByAsset(AActor* TargetActor, TSoftObjectPtr<USoundBase> AudioAsset, FVector Postion /*= FVector::ZeroVector*/, EAUDIOCOMPTYLE AudioCompType /*= EAUDIOCOMPTYLE::NONE*/, bool bIsLoop /*= false*/, USceneComponent* AttachComp /* = nullptr*/, float StartTime /*= 0.0f*/)
{
	if (!CheckPlayVoice(CSTORY_VOICE_TYPE::SOUND3D))return nullptr;
	UCS3AudioComponent* SkillAudioComponent = CreateAudioComponent(TargetActor, Postion, AttachComp);
	if (IsValid(SkillAudioComponent))
	{
		SetAudioComponent_AudioAsset(TargetActor, SkillAudioComponent, bIsLoop, StartTime, AudioAsset, AudioCompType);
	}
	return SkillAudioComponent;
}

void AAudioManager::StopAllSkill3DSound()
{
	///中止播放音效
	for (auto AudioComponent : SkillEffectAudioComponent)
	{
		if (!IsValid(AudioComponent)) continue;
		if (AudioComponent->IsPlaying())
		{
			AudioComponent->Stop();
			AudioComponent->Sound = nullptr;
			AudioComponent->DestroyComponent();
		}
	}
	SkillEffectAudioComponent.Empty();
}

void AAudioManager::Stop3DSound(UCS3AudioComponent* AudioComponent)
{
	if (IsValid(AudioComponent))
	{
		if (AudioComponent->IsPlaying())
		{
			AudioComponent->Stop();
		}
		AudioComponent->Sound = nullptr;
		if (Audio3DComponent.Contains(AudioComponent))
		{
			Audio3DComponent.Remove(AudioComponent);
			AudioComponent->DestroyComponent();
			return;
		}
		if (SkillEffectAudioComponent.Contains(AudioComponent))
		{
			SkillEffectAudioComponent.Remove(AudioComponent);
			AudioComponent->DestroyComponent();
		}
	}
}

void AAudioManager::PausedAll3DSound(bool bIsPaused /*= false*/)
{
	TArray<UAudioComponent*> All3DComponent = Audio3DComponent;
	if (SkillEffectAudioComponent.Num() > 0)
	{
		All3DComponent.Append(SkillEffectAudioComponent);
	}

	///中止播放音效
	for (auto AudioComponent : All3DComponent)
	{
		if (!IsValid(AudioComponent)) continue;

		if (bIsPaused)
		{
			if (AudioComponent->IsPlaying())
			{
				AudioComponent->SetPaused(bIsPaused);
				AudioComponent->Sound = nullptr;
			}
		}
		else
		{
			AudioComponent->SetPaused(bIsPaused);
		}
	}
}

void AAudioManager::StopAll3DSound()
{
	SCOPE_CYCLE_COUNTER(STAT_StopAll3DSound);
	StopAllSkill3DSound();
	///中止播放音效
	for (auto AudioComponent : Audio3DComponent)
	{
		if (!IsValid(AudioComponent)) continue;
		if (AudioComponent->IsPlaying())
		{
			AudioComponent->Stop();
			AudioComponent->Sound = nullptr;
			AudioComponent->DestroyComponent();
		}
	}
	Audio3DComponent.Empty();
}

void AAudioManager::On3DAudioFinishedNative(UAudioComponent* AudioComponent)
{
	Remove3DAudioComponent(AudioComponent);
}

void AAudioManager::Remove3DAudioComponent(UAudioComponent* AudioComponent)
{
	if (!IsValid(AudioComponent))
	{
		return;
	}
	for (auto comp : SkillEffectAudioComponent)
	{
		if (comp == AudioComponent)
		{
			SkillEffectAudioComponent.Remove(AudioComponent);
			return;
		}
	}
	for (auto comp : Audio3DComponent)
	{
		if (comp == AudioComponent)
		{
			Audio3DComponent.Remove(AudioComponent);
			return;
		}
	}
}

UCS3AudioComponent* AAudioManager::CreateAudioComponent(AActor* TargetActor, FVector Postion /*= FVector::ZeroVector*/, USceneComponent* AttachComp /*= nullptr*/)
{
	SCOPE_CYCLE_COUNTER(STAT_CreateAudioComponent);
	FString AudioComponentName = "SkillAudioComponent" + INT_TO_FSTRING(FMath::RandHelper(MAX_int32));
	UCS3AudioComponent* SkillAudioComponent;
	if (IsValid(TargetActor))
	{		
		 SkillAudioComponent = NewObject<UCS3AudioComponent>(TargetActor, FSTRING_TO_FNAME(AudioComponentName));
	}
	else
	{
		SkillAudioComponent = NewObject<UCS3AudioComponent>(UUECS3GameInstance::Instance->GetWorld(), FSTRING_TO_FNAME(AudioComponentName));
	}
	SkillAudioComponent->RegisterComponent();
	SkillAudioComponent->bAutoDestroy = true;
	SkillAudioComponent->bOverrideAttenuation = true;
	SkillAudioComponent->bStopWhenOwnerDestroyed = true;

	if (Postion != FVector::ZeroVector)
	{
		SkillAudioComponent->SetWorldLocation(Postion);
	}
	else if (IsValid(AttachComp))
	{
		SkillAudioComponent->AttachToComponent(AttachComp, FAttachmentTransformRules::KeepRelativeTransform);
	}
	else
	{
		if (IsValid(TargetActor))
		{
			if (IsValid(Cast<AServerCharacter>(TargetActor)))
			{
				UCapsuleComponent *CapsuleComponent = Cast<AServerCharacter>(TargetActor)->GetCapsuleComponent();
				USceneComponent *SceneComponent = Cast<USceneComponent>(CapsuleComponent);
				SkillAudioComponent->AttachToComponent(SceneComponent, FAttachmentTransformRules::KeepRelativeTransform);
			}
			else
			{
				SkillAudioComponent->AttachToComponent(TargetActor->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
			}
		}
		else
		{
			SkillAudioComponent->AttachToComponent(RootComponent, FAttachmentTransformRules::KeepRelativeTransform);
		}
	}
	return SkillAudioComponent;
}

bool AAudioManager::CheckNewAudioComponent(CSTORY_VOICE_TYPE VoiceType)
{
	switch (VoiceType)
	{
	case CSTORY_VOICE_TYPE::SOUND3D:
	{
		//if (VoiceType == CSTORY_VOICE_TYPE::VOICE)return true;
		break;
	}
	}
	return false;
}

bool AAudioManager::CheckHideVoice(CSTORY_VOICE_TYPE VoiceType)
{
	SCOPE_CYCLE_COUNTER(STAT_CheckHideVoice);
	TArray<int32> AllHideVoiceTypes = DefualtHideVoiceTypes;
	if (HideVoiceTypes.Num() > 0)
	{
		AllHideVoiceTypes.Append(HideVoiceTypes);
	}

	for (auto& HideNum : AllHideVoiceTypes)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AStoryManager::PausedVoice -> HideType[%d]~"), HideNum);
		switch (HideNum)
		{
		case 0:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::VOICE)return true;
			break;
		}
		case 1:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::FIGHTNUSIC)return true;
			break;
		}
		case 2:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::BGMUSIC)return true;
			break;
		}
		case 3:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::CLIENTVOICE)return true;
			break;
		}
		case 4:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::SOUND3D)return true;
			break;
		}
		case 5:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::ENVIRONMENT)return true;
			break;
		}
		case 6:
		{
			if (VoiceType == CSTORY_VOICE_TYPE::WEATHER)return true;
			break;
		}
		default: CS3_Warning(TEXT("AAudioManager::CheckHideVoice ->  HideNum[%d] is not found~"), HideNum); break;
		}
	}
	return false;
}

void AAudioManager::SetHideVoice(TArray<FString> HideTypes)
{
	HideVoiceTypes.Reset();
	
	for (auto& Elem : HideTypes)
	{
		if (Elem.IsEmpty())continue;
		int32 HideNum = FCString::Atoi(*Elem);
		HideVoiceTypes.Add(HideNum);
	}
}

void AAudioManager::SetDefualtHideVoiceTypes(TArray<FString> HideTypes)
{
	DefualtHideVoiceTypes.Reset();
	for (auto& Elem : HideTypes)
	{
		if (Elem.IsEmpty())continue;
		int32 HideNum = FCString::Atoi(*Elem);
		DefualtHideVoiceTypes.Add(HideNum);
	}
}

void AAudioManager::SetAudioComponent_AudioAsset(AActor* TargetActor, UCS3AudioComponent* AudioComponent, bool bIsLoop, float StartTime, TSoftObjectPtr<USoundBase> AudioAsset, EAUDIOCOMPTYLE AudioCompType)
{
	if (AudioAsset.IsValid() && IsValid(AudioComponent))
	{
		AudioComponent->SetVolumeMultiplier(GetEffVol());	// 3D声音音量使用VoiceVol
		AudioComponent->Sound = AudioAsset.Get();
		if (Cast<USoundWave>(AudioAsset.Get()) && bIsLoop == true)
		{
			Cast<USoundWave>(AudioAsset.Get())->bLooping = bIsLoop;
		}
		AudioComponent->Play(StartTime);
		AudioComponent->OnVirtualAudioFinishedNative.AddUObject(this, &AAudioManager::On3DAudioFinishedNative);
		if (AudioCompType == EAUDIOCOMPTYLE::SKILL)
		{
			SkillEffectAudioComponent.Add(AudioComponent);///保存声音组件，用于结束时终止声音
			if (IsValid(TargetActor) && IsValid(Cast<AServerCharacter>(TargetActor)))
			{
				Cast<AServerCharacter>(TargetActor)->SkillCastAudioComponent = AudioComponent;
			}
		}
		else
		{
			Audio3DComponent.Add(AudioComponent);
		}
	}
}

void AAudioManager::TogglePlayAudioSystem()
{
	if (bEnableAudioPlay)
	{
		bEnableAudioPlay = false;
		ClearAudioData();
	}
	else
	{
		bEnableAudioPlay = true;
		PlaySceneAndEnvironmentMusic();
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerController->CS3ConSoleMgr))
	{
		PlayerController->CS3ConSoleMgr->SetEnableAudioSystem(bEnableAudioPlay);
	}
}

bool AAudioManager::PlayPreviewSound(const FString& AudioPath)
{
	USoundBase* SoundAsset = (USoundBase*)UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(AudioPath));
	if (IsValid(SoundAsset) && IsValid(PreviewSoundComp))
	{
		if (PreviewSoundComp->IsPlaying())
			PreviewSoundComp->Stop();
		PreviewSoundComp->SetVolumeMultiplier(1.f);
		PreviewSoundComp->SetSound(SoundAsset);
		PreviewSoundComp->Play(0.f);
		return true;
	}
	return false;
}

void AAudioManager::StopPreviewSound()
{
	if (!IsValid(PreviewSoundComp)) return;
	if (PreviewSoundComp->IsPlaying())
	{
		PreviewSoundComp->Stop();
		PreviewSoundComp->Sound = nullptr;
	}
}

void AAudioManager::PlayEnvironmentSound()
{
	StopEnvironmentSound();
	if (!CheckPlayVoice(CSTORY_VOICE_TYPE::ENVIRONMENT))return;
	const FString SpaceId = GetCurSpaceId();
	USoundBase* SoundAsset = GetEnvironmentMusicAsset(SpaceId);
	if (IsValid(SoundAsset))
	{
		SetEnvironmentMusicVol(GetEffVol());
		EnvironmentSoundComp->SetSound(SoundAsset);
		EnvironmentSoundComp->Play();
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::PlayEnvironmentSound -> Current SoundAsset is Null "));
	}
}

void AAudioManager::StopEnvironmentSound()
{
	if (EnvironmentSoundComp->IsPlaying())
	{
		EnvironmentSoundComp->Stop();
		EnvironmentSoundComp->Sound = nullptr;
	}
}

bool AAudioManager::IsPlaying(const FString & VoiceId)
{
	if (VoiceDelayList.Num() > 0 && VoiceComp->IsPlaying())
	{
		///<VoiceComp 当前是否正在播放
		if (!VoiceId.Compare(TEXT("")))
		{
			return true;
		}
		if (!VoiceDelayList[0].Id.Compare(VoiceId))
			return true;
	}
	return false;
}

void AAudioManager::OnVoicesFinishedCB(FVOICE_DATA& VoiceData)
{
	RefreshVoiceData(VoiceData);
	NotifyPerformanceInterfaceToPlayNext();
	
	URolePerformanceInterface * Interface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
	if (Interface)
	{
		FString voiceID = VoiceData.Id;
		Interface->RPC_StopPlaySound(voiceID);
	}
}

void AAudioManager::OnSceneAudioFinishedNative(UAudioComponent* AudioComponent)
{	
	if (UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		bool bFightState = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->IsState(ENTITY_STATE::EntityStateFight);
		
		if (AudioComponent == BgMusicComp)
		{
			BgMusicComp->OnVirtualAudioFinishedNative.Clear();
			if (!bFightState)
			{
				bIsPlaySceneMusic = true;				
			}			
		}
		if (AudioComponent == FightMusicComp)
		{
			FightMusicComp->OnVirtualAudioFinishedNative.Clear();
			if (bFightState)
			{
				bIsPlayFightMusic = true;
			}			
		}
	}
}

void AAudioManager::RefreshVoiceData(FVOICE_DATA& VoiceData)
{
	// 移除播放第一个语音
	if (VoiceDelayList.Num() > 0)
	{
		if (StoryVoiceList.Contains(VoiceDelayList[0].AudioId))
		{
			StoryVoiceList.Remove(VoiceDelayList[0].AudioId);
		}
		VoiceData = VoiceDelayList[0];
		VoiceDelayList.RemoveAt(0);

		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::OnVoicesFinishedCB -> Current VoiceDelayList Num[%d]"), VoiceDelayList.Num());
	}
}

void AAudioManager::NotifyPerformanceInterfaceToPlayNext()
{
	URolePerformanceInterface * Interface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
	if (Interface)
	{
		Interface->PlayNext();
	}
}

void AAudioManager::AddStoryAudio(const FString & Id)
{
	StoryVoiceList.Add(Id);
}

void AAudioManager::ResetStoryAudio()
{
	StoryVoiceList.Empty();
}

void AAudioManager::PlayWeatherSound(TSoftObjectPtr<USoundBase> AudioAsset)
{
	if (!CheckPlayVoice(CSTORY_VOICE_TYPE::WEATHER))return;
	if (AudioAsset.ToSoftObjectPath().IsValid() && IsValid(WeatherSoundComp))
	{
		USoundBase* SoundAsset = Cast<USoundBase>(UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(AudioAsset.ToSoftObjectPath()));
		if (IsValid(SoundAsset))
		{
			SetWeatherMusicVol(GetMasterVol());
			WeatherSoundComp->SetSound(SoundAsset);
			WeatherSoundComp->Play();
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::PlayEnvironmentSound -> Current SoundAsset is Null "));
		}
	}
}

void AAudioManager::StopWeatherSound()
{
	if (IsValid(WeatherSoundComp) && WeatherSoundComp->IsPlaying())
	{
		WeatherSoundComp->Stop();
		WeatherSoundComp->Sound = nullptr;
	}
}

void AAudioManager::UpdateWeatherComp(USceneComponent* SceneComp)
{
	if (!IsValid(WeatherSoundComp))
	{
		WeatherSoundComp = NewObject<UCS3AudioComponent>(this, TEXT("WeatherSoundComp"));
	}
	if (IsValid(WeatherSoundComp) && IsValid(SceneComp))
	{
		FAttachmentTransformRules AttachmentTransformRules(EAttachmentRule::SnapToTarget, EAttachmentRule::KeepWorld, EAttachmentRule::KeepWorld, false);
		WeatherSoundComp->AttachToComponent(SceneComp, AttachmentTransformRules);
	}
}

void AAudioManager::UnBindWeatherSoundComp()
{
	if (IsValid(WeatherSoundComp) )
	{	
		if (IsValid(WeatherSoundComp->GetAttachParent()))
		{
			WeatherSoundComp->DetachFromComponent(FDetachmentTransformRules::KeepRelativeTransform);
		}		
	}
}

void AAudioManager::PausedWeather(bool bIsPaused /*= false*/)
{
	if (IsValid(WeatherSoundComp))
	{
		if (WeatherSoundComp->IsPlaying() && bIsPaused)
		{
			WeatherSoundComp->SetPaused(bIsPaused);
		}
		if (!bIsPaused && IsValid(WeatherSoundComp->Sound))
		{
			WeatherSoundComp->SetPaused(bIsPaused);
		}
	}
}

void AAudioManager::SetWeatherMusicVol(float Vol)
{
	if (Vol < 0.00011f)
	{
		if (IsValid(WeatherSoundComp))
		{
			WeatherSoundComp->SetVolumeMultiplier(0.00011f);
		}
	}
	else
	{
		if (IsValid(WeatherSoundComp))
		{
			WeatherSoundComp->SetVolumeMultiplier(Vol);
		}
	}
}

void AAudioManager::PlaySoundUI(const FString& AssetId)
{
	if (USoundBase* sound = GetAudioAsset(AssetId))
	{
		UGameplayStatics::PlaySound2D(this, sound, GetEffVol());
	}
}

void AAudioManager::PlaySceneMusic(bool IsPlayBgMusic)
{
	SCOPE_CYCLE_COUNTER(STAT_PlaySceneMusic);
	bool IsFindPlayList = false;
	TSoftObjectPtr<USoundBase> SoundAssetPtr = GetSceneMusicAsset(IsPlayBgMusic, IsFindPlayList);
	
	if (IsValid(SoundAssetPtr.Get()))
	{
		PlaySceneMusicByAsset(IsPlayBgMusic, SoundAssetPtr.Get(), IsFindPlayList);
		return;
	}
	IsPlayBgMusic ? BgMusicComp->SetAssertLoadState(Load_Assert_State::Assert_Loading) : FightMusicComp->SetAssertLoadState(Load_Assert_State::Assert_Loading);
	if (SoundAssetPtr.ToSoftObjectPath().IsValid())
	{
		TWeakObjectPtr<AAudioManager> DelayThisPtr(this);
		UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, SoundAssetPtr.ToSoftObjectPath(), FStreamableDelegate::CreateLambda([DelayThisPtr, IsPlayBgMusic, SoundAssetPtr, IsFindPlayList]()
		{
			if (DelayThisPtr.IsValid() && IsValid(SoundAssetPtr.Get()))
			{
				AAudioManager* DelayThis = DelayThisPtr.Get();	
				if (IsPlayBgMusic)
				{
					DelayThis->BgMusicComp->SetAssertLoadState(Load_Assert_State::Assert_Ready);
				}
				else
				{
					DelayThis->FightMusicComp->SetAssertLoadState(Load_Assert_State::Assert_Ready);
				}

				if (UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())
				{
					bool bFightState = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->IsState(ENTITY_STATE::EntityStateFight);
					if (bFightState!= IsPlayBgMusic)
					{
						DelayThis->PlaySceneMusicByAsset(IsPlayBgMusic, SoundAssetPtr.Get(), IsFindPlayList);
					}
					if (DelayThis->bDelayStopMusic)
					{
						DelayThis->bDelayStopMusic = false;
						DelayThis->StopSceneMusic(IsPlayBgMusic);
					}
				}
				else
				{
					DelayThis->PlaySceneMusicByAsset(IsPlayBgMusic, SoundAssetPtr.Get(), IsFindPlayList);
				}
			}
		}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_MEDIA);
	}
}

void AAudioManager::StopSceneMusic(bool IsPlayBgMusic)
{
	if (IsPlayBgMusic)
	{	
		if (BgMusicComp->Sound)
		{
			BgMusicComp->OnVirtualAudioFinishedNative.Clear();
			
			BgMusicComp->FadeOut(BgMusicFadeTimer, 0.0f);		
			BgMusicComp->Sound = nullptr;
			CurrentBgMusicIndex = 0;
			bBgMusicRandomFinished = false;			
		}
		else if(BgMusicComp->IsAssertLoadState(Load_Assert_State::Assert_Loading))
		{
			bDelayStopMusic = true;
		}
	}
	else
	{		
		if (FightMusicComp->Sound )
		{
			FightMusicComp->OnVirtualAudioFinishedNative.Clear();			
			FightMusicComp->FadeOut(FightMusicFadeTimer, 0.0f);			
			FightMusicComp->Sound = nullptr;	
			CurrentFightMusicIndex = 0;
			bFightMusicRandomFinished = false;			
		}
		else if(FightMusicComp->IsAssertLoadState(Load_Assert_State::Assert_Loading))
		{
			bDelayStopMusic = true;
		}
	}
}

void AAudioManager::LoopPlaySceneMusicByPlayerState(bool bIsBgMusic, bool bIsPlay, bool bByPlayerState)
{
	SCOPE_CYCLE_COUNTER(STAT_LoopPlaySceneMusicByPlayerState);
	if (bByPlayerState)
	{
		if (UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
		{
			bool bFightState = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->IsState(ENTITY_STATE::EntityStateFight);

			if (bIsPlay)
			{
				
				if (bFightState)
				{
					bIsPlayFightMusic = true;
				}
				else
				{
					bIsPlaySceneMusic = true;
				}
			}
			else
			{				
				if (bFightState)
				{
					bIsStopFightMusic = true;
				}
				else
				{
					bIsStopSceneMusic = true;
				}
			}
		}
		return;
	}

	if (bIsBgMusic)
	{
		if (bIsPlay)
		{
			bIsPlaySceneMusic = true;	
		}
		else
		{
			bIsStopSceneMusic = true;
		}
	}
	else
	{
		if (UGolbalBPFunctionLibrary::GetCS3PlayerCharacter() && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
		{
			bool bFightState = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->IsState(ENTITY_STATE::EntityStateFight);
			if (bFightState)
			{
				if (bIsPlay)
				{
					bIsPlayFightMusic = true;
				}
				else
				{
					bIsStopFightMusic = true;
				}
			}
		}
	}
}

void AAudioManager::SetBgVol(float inVolume)
{
	if (BgMusicComp->IsPlaying())
	{
		BgMusicComp->SetVolumeMultiplier(inVolume);
	}
	if (FightMusicComp->Sound)
	{
		FightMusicComp->SetVolumeMultiplier(inVolume);
	}
}

void AAudioManager::SetSingleVoiceVol(float inVol)
{
	if (VoiceComp->IsPlaying())
	{
		VoiceComp->SetVolumeMultiplier(inVol);
	}
}

void AAudioManager::SetVoiceVol(float inVolume)
{
	if (ClientVoiceComp->IsPlaying())
	{
		ClientVoiceComp->SetVolumeMultiplier(inVolume);
	}
}

void AAudioManager::SetEffVol(float inVolume)
{
	for (auto AudioComp : SkillEffectAudioComponent)
	{
		if (IsValid(AudioComp) && AudioComp->IsPlaying())
		{
			AudioComp->SetVolumeMultiplier(inVolume);
		}
	}
	for (auto AudioComp : Audio3DComponent)
	{
		if (IsValid(AudioComp) && AudioComp->IsPlaying())
		{
			AudioComp->SetVolumeMultiplier(inVolume);
		}
	}

	if (IsValid(EnvironmentSoundComp)&& EnvironmentSoundComp->IsPlaying())
	{
		EnvironmentSoundComp->SetVolumeMultiplier(inVolume);
	}
}

void AAudioManager::SetBgEffVol(float inVolume)
{
	if (BgEffectComp->IsPlaying())
	{
		BgEffectComp->SetVolumeMultiplier(inVolume);
	}
}

void AAudioManager::SetMasterVol(float inVolume)
{
	MasterSoundClass->Properties.Volume = inVolume; // FMath::Max(inVolume, 0.01f);
}


float AAudioManager::GetBgVol()
{
	if (UUECS3GameInstance::Instance&&
		UUECS3GameInstance::Instance->LocalDataSaveManager&&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData)
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetBgVol();
	}
	return 1.0f;
}

float AAudioManager::GetVoiceVol()
{
	if (UUECS3GameInstance::Instance&&
		UUECS3GameInstance::Instance->LocalDataSaveManager&&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData)
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetVoiceVol();
	}
	return 1.0f;
}

float AAudioManager::GetEffVol()
{
	if (UUECS3GameInstance::Instance&&
		UUECS3GameInstance::Instance->LocalDataSaveManager&&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData)
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetEffVol();
	}
	return 1.0f;
}

float AAudioManager::GetBgEffVol()
{
	if (UUECS3GameInstance::Instance&&
		UUECS3GameInstance::Instance->LocalDataSaveManager&&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData)
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetEffVol();
	}
	return 1.0f;
}

float AAudioManager::GetMasterVol()
{
	if (UUECS3GameInstance::Instance&&
		UUECS3GameInstance::Instance->LocalDataSaveManager&&
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData)
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->GetMainVolume();
	}
	return 1.0f;
}

void AAudioManager::OnLeaveWorld()
{
	ClearAudioData();
}

void AAudioManager::ClearAudioData()
{
	SCOPE_CYCLE_COUNTER(STAT_ClearAudioData);
	StopVoice();
	ClientVoiceStop();
	StopSceneMusic(true);
	StopSceneMusic(false);
	// 关闭预览声音播放
	StopPreviewSound();
	StopEnvironmentSound();
	StopWeatherSound();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("AAudioManager::ClearAudioData -> End"));
}

CONTROL_COMPILE_OPTIMIZE_END

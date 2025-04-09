// Fill out your copyright notice in the Description page of Project Settings.

#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PreloadingBehavior.h"
#include "Util/CS3Debug.h"
#include "Manager/GameStatus.h"
#include "Manager/StoryManager.h"
#include "Manager/ParticleManager.h"
#include "Manager/QTEManager.h"
#include "Manager/ResourceManager.h"
#include "Manager/LoginManager.h"
#include "Manager/PlaneTriggerManager.h"
#include "CS3Base/UIManager.h"
#include "Entity.h"
#include "../Entity/Role/CS3Role.h"
#include "GameData/GameDefault.h"
#include "GameData/ConstDataBP.h"
#include "Actor/ServerCharacter.h"
#include "Level/SelectCampLevel.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/CharacterRideManager.h"
#include "Manager/ActionManager.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Manager/LevelManager.h"
#include "Manager/MessageManager.h"
#include "Manager/AudioManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/BuffManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/MapManager.h"
#include "CS3Base/UIDockManager.h"
#include "CS3Base/UIFixerManager.h"
#include "Manager/QuestManager.h"
#include "Manager/BuffEntityVisibleManager.h"
#include "GameData/MessageID.h"
#include "Manager/LoaderManager.h"
#include "GameData/SavePlayerData.h"
#include "GameData/AreaWallData.h"
#include "Manager/VisibleManager.h"
#include "Manager/QuestEntityVisibleManager.h"
#include "Manager/EventManager.h"
#include "Manager/TipsManager.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "GameData/Item/ItemFactory.h"
#include "Manager/EmoteManager.h"
#include "Manager/SpaceDynamicEffectManager.h"
#include "Manager/DecalManager.h"
#include "Manager/HyperlinkManager.h"
#include "Manager/TextParseManager.h"
#include "Manager/AutoNavigatePathMgr.h"
#include "Manager/ForceManager.h"
#include "AutoTest/AutoTestManager.h"
#include "AutoTest/CS3Listener.h"
#include "Manager/TutorialManager.h"
#include "Manager/SystemSwitchManager.h"
#include "Manager/CrossMapNavigateMgr.h"
#include "AutoTest/GMCommand/ClientGMCMDToServer.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/TextShieldMgr.h"
#include "Manager/TimeManager.h"
#include "Manager/AutoFightMar.h"
#include "Manager/MediaPlayerManager.h"
#include "Manager/SkillManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/GameplayEventManager.h"
#include "Manager/ShapeManager.h"
#include "Manager/ModifyFaceManager.h"
#include "Manager/HeadManager.h"
#include "Manager/QuickBarManager.h"
#include "GameData/StrToClass.h"
#include "GameData/ProfessionData.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/TexturePath.h"
#include "Level/NewCreateRoleLevel.h"
#include "Level/NewSelectRoleLevel.h"
#include "Util/ConvertUtil.h"
#include "GameData/LocalDataSave/LocalUserSettingData.h"
#include "Util/ImageLoader.h"
#include "Skill/SkillLoader.h"
#include "skill/EffectLoader.h"
#include "skill/BuffLoader.h"
#include "PreloadingSubsystem.h"

KBEngine::KBEngineApp * UUECS3GameInstance::pKBEApp = nullptr;
UUECS3GameInstance* UUECS3GameInstance::Instance = nullptr;
FCS3PostLoadMapDelegate UUECS3GameInstance::LevelBeginPlayDelegate;

void UUECS3GameInstance::Init()
{
	
	// 根据配置默认设置屏幕是否显示输出
	{
		const UGameDefault& GameDefault_ = *UGameDefault::StaticClass()->GetDefaultObject<UGameDefault>();
		GAreScreenMessagesEnabled = GameDefault_.IsEnabledScreenPrint;
	}

	UUECS3GameInstance::Instance = this;

	GameDefault = NewObject<UGameDefault>();
	if (GameDefault->bOpenNotifyObject)
	{
		CreateListener = new CS3CreateListener();//UUECS3GameInstance::BeginDestroy()销毁
		DeleteListener = new CS3DeleteListener();//UUECS3GameInstance::BeginDestroy()销毁
		GUObjectArray.AddUObjectCreateListener(CreateListener);
		GUObjectArray.AddUObjectDeleteListener(DeleteListener);
	}

	TimerManager = Super::TimerManager;
	ResourceManager = UResourceManager::GetInstance();
	CfgManager = UCfgManager::GetInstance();
	ConstDataBP = UConstDataBP::GetInstance();
	AreaWallData = UAreaWallData::GetInstance();
	ActionManager = UActionManager::GetInstance();
	MessageManager = UMessageManager::GetInstance();
	SkillLoader = USkillLoader::GetInstance();
	EffectLoader = UEffectLoader::GetInstance();
	BuffLoader = UBuffLoader::GetInstance();
	SkillManager = USkillManager::GetInstance();
	BuffManager = UBuffManager::GetInstance();
	CustomCursorManager = UCustomCursorManager::GetInstance();
	PlaneTriggerManager = UPlaneTriggerManager::GetInstance();
	UIDockManager = UUIDockManager::GetInstance();
	UIFixerManager = UUIFixerManager::GetInstance();
	QuestManager = UQuestManager::GetInstance();
	DecalManager = UDecalManager::GetInstance();
	ForceManager = UForceManager::GetInstance();

	GMessageID = NewObject<UMessageID>();
	SaveData = NewObject<USavePlayerData>();

	VisibleManager = UVisibleManager::GetInstance();
	QuestEntityVisibleManager = UQuestEntityVisibleManager::GetInstance();
	BuffEntityVisibleManager = UBuffEntityVisibleManager::GetInstance();

	SpaceEntityRelationMgr = USpaceEntityRelationMgr::GetInstance();
	SpaceDynamicEffectManager = USpaceDynamicEffectManager::GetInstance();

	////////////////////////////////////global Manager with use in Blueprint/////////////////////////
	GameStatus = UGameStatus::GetInstance();
	LoginManager = ULoginManager::GetInstance();
	LoginManager->Init();
	LevelManager = ULevelManager::GetInstance();
	MapManager = UMapManager::GetInstance();
	GLoaderManager = UGLoaderManager::GetInstance();
	GStoryManager = UGStoryManager::GetInstance();
	MediaPlayerManager = UMediaPlayerManager::GetInstance();
	GEventManager = UGEventManager::GetInstance();
	GameplayEventManager = UGameplayEventManager::GetInstance();
	GUIManager = UGUIManager::GetInstance();
	HyperlinkManager = UHyperlinkManager::GetInstance();

	TipsManager = UTipsManager::GetInstance();
	ItemFactory = UItemFactory::GetInstance();
	EmoteManager = UEmoteManager::GetInstance();
	EmoteManager->Init();
	AutoTestManager = UAutoTestManager::GetInstance();
	TutorialManager = UTutorialManager::GetInstance();
	TutorialManager->LoadCfg();
	SystemSwitchManager = USystemSwitchManager::GetInstance();
	SystemSwitchManager->LoadCfg();
	ControllerModeMgr = UControllerModeMgr::GetInstance();
	ControllerModeMgr->Init();
	OperationModeMgr = UOperationModeMgr::GetInstance();
	OperationModeMgr->Init();
	QTEManager = UQTEManager::GetInstance();
	CharacterRideManager = UCharacterRideManager::GetInstance();
	AutoFightMar = UAutoFightMar::NewInstance();
	HeadManager = AHeadManager::GetInstance();
	QuickBarManager = UQuickBarManager::GetInstance();
	QuickBarManager->Init();
	////////////////////////////////////global Manager with use in Blueprint/////////////////////////

	LocalDataSaveManager = ULocalDataSaveManager::GetInstance();
	LocalDataSaveManager->Init();
	ParticleManager = UParticleManager::GetInstance();
	AudioManager = AAudioManager::GetInstance();
	TextParseMgr = UTextParseManger::GetInstance();
	AutoNavigatePathMgr = UAutoNavigatePathMgr::GetInstance();
	CrossMapNavigateMgr = UCrossMapNavigateMgr::GetInstance();
	ClientGMCMDToServer = UClientGMCMDToServer::GetInstance();
	TextShieldMgr = UTextShieldMgr::GetInstance();
	TimeManager = UTimeManager::GetInstance();
	CustomTimerManager = UCustomTimerManager::GetInstance();
	ShapeManager = UShapeManager::GetInstance();
	ModifyFaceManager = UModifyFaceManager::GetInstance();
	ImageLoader = UImageLoader::GetInstance();	
	bIsFristBindPostLoadMap = true;
	bIsGameWindowActive = true;

	GameWindowHandle = FSlateApplication::Get().OnApplicationActivationStateChanged().AddUObject(this, &UUECS3GameInstance::CheckApplicationActivation);
	//绑定设置通知
	LocalDataSaveManager->LocalUserSettingData->OnVideoSettingChange.AddUObject(ParticleManager, &UParticleManager::UpdateParticleDiaplayConfig);

	CheckLanderSystemSetting();

	//------------开始后台异步加载永不释放的核心资源
	BackstageAsyncLoad_Table_One(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS, FStrToClass, ClassPath.ToSoftObjectPath());
	BackstageAsyncLoad_Table_One(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ASYNCLOAD_UI_TEXTURE_DATA, FBackstageAsyncLoadTexture, TexturePath.ToSoftObjectPath());
	BackstageAsyncLoad_Table_One(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF, FBUFF_TABLE_DATA, BuffIcon.ToSoftObjectPath());
	BackstageAsyncLoad_Table_One(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_BUFF_TEST, FBUFF_TABLE_DATA, BuffIcon.ToSoftObjectPath());

	UGameInstance::Init();

	// 调用所有UCS3PreloadingBehavior::OnPostCS3GameInstanceInit
	{
		TArray<UPreloadingBehavior*> AllPreloadingBehavior = GetSubsystem<UPreloadingSubsystem>()->GetAllPreloadingBehavior();
		for (auto PreloadingBehavior : AllPreloadingBehavior)
		{
			if (UCS3PreloadingBehavior* CS3PreloadingBehavior = Cast<UCS3PreloadingBehavior>(PreloadingBehavior))
			{
				CS3PreloadingBehavior->OnPostCS3GameInstanceInit(this);
			}
		}
	}
}

void UUECS3GameInstance::BeginDestroy()
{
	if (IsValid(GameDefault) && GameDefault->bOpenNotifyObject)
	{
		GUObjectArray.RemoveUObjectCreateListener(CreateListener);
		GUObjectArray.RemoveUObjectDeleteListener(DeleteListener);
		delete CreateListener;
		CreateListener = nullptr;
		delete DeleteListener;
		DeleteListener = nullptr;
	}
	Super::BeginDestroy();
	CS3PC = nullptr;
}

void UUECS3GameInstance::FinishDestroy()
{
	Super::FinishDestroy();
	if (GIsEditor)
	{
		SAFE_DELETE(Instance);
	}
}

void UUECS3GameInstance::Shutdown()
{
	bIsShutDown = true;
	///<游戏停止保存当前是否全屏和分辨率
	if (IsValid(LocalDataSaveManager->LocalUserSettingData))
	{
		LocalDataSaveManager->LocalUserSettingData->SaveVideoSettingDataToConfig();
	}
	///<游戏停止保存3D半身像配置表
	if (IsValid(HeadManager))
	{
		HeadManager->StopHalfHeadSetting();
	}
	if (IsValid(GStoryManager))
	{
		//停止播放镜头并清除镜头缓存
		GStoryManager->StopSequence();
		GStoryManager->ClearStoryAsset();
	}
	if (GameWindowHandle.IsValid())
	{
		FSlateApplication::Get().OnApplicationActivationStateChanged().Remove(GameWindowHandle);
	}
	ResourceManager->ReleaseAllHandles();
	CustomTimerManager->ClearAllTimer();
	ConstDataBP = nullptr;
	ResourceManager = nullptr;
	CfgManager = nullptr;
	ParticleManager = nullptr;
	LoginManager = nullptr;
	GStoryManager = nullptr;
	UIDockManager = nullptr;
	UIFixerManager = nullptr;
	LevelManager = nullptr;
	ActionManager = nullptr;
	MessageManager = nullptr;
	GameStatus = nullptr;
	AudioManager = nullptr;
	LocalDataSaveManager = nullptr;
	SkillManager = nullptr;
	QuestManager = nullptr;
	BuffManager = nullptr;
	CustomCursorManager = nullptr;
	MapManager = nullptr;
	PlaneTriggerManager = nullptr;
	GMessageID = nullptr;
	GLoaderManager = nullptr;
	VisibleManager = nullptr;
	QuestEntityVisibleManager = nullptr;
	BuffEntityVisibleManager = nullptr;
	GEventManager = nullptr;
	GameplayEventManager = nullptr;
	GUIManager = nullptr;
	HyperlinkManager = nullptr;
	TipsManager = nullptr;
	SpaceEntityRelationMgr = nullptr;
	SpaceDynamicEffectManager = nullptr;
	ItemFactory = nullptr;
	EmoteManager = nullptr;
	AreaWallData = nullptr;
	DecalManager = nullptr;
	TextParseMgr = nullptr;
	AutoNavigatePathMgr = nullptr;
	CrossMapNavigateMgr = nullptr;
	ForceManager = nullptr;
	AutoTestManager = nullptr;
	TextShieldMgr = nullptr;
	ControllerModeMgr = nullptr;
	OperationModeMgr = nullptr;
	TimeManager = nullptr;
	CustomTimerManager = nullptr;
	SystemSwitchManager = nullptr;
	HeadManager = nullptr;
	QuickBarManager = nullptr;
	ImageLoader = nullptr;
	SkillLoader = nullptr;
	EffectLoader = nullptr;
	BuffLoader = nullptr;

	//此处做特殊处理是因为这个管理器在编辑器模式下也可以使用
	UDecalManager::ClearInstance();

	KBEngine::KBEngineApp *pTempKBEApp = pKBEApp;
	UUECS3GameInstance::pKBEApp = nullptr;
	SAFE_DELETE(pTempKBEApp);
	
	//TutorialManager销毁需要在pKBEApp之后
	TutorialManager = nullptr;
	Super::Shutdown();

}

void UUECS3GameInstance::RoleEnterWorld(FString Name)
{
}


void UUECS3GameInstance::ReStoreUI()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ReStoreUI"));
}

bool UUECS3GameInstance::ProcessConsoleExec(const TCHAR* Cmd, FOutputDevice& Ar, UObject* Executor)
{
	bool ret = Super::ProcessConsoleExec(Cmd, Ar, Executor);
	if (!ret && UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())
	{
			ret = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->ProcessConsoleExec(Cmd, Ar, Executor);
	}
	return ret;
}

void UUECS3GameInstance::LoadComplete(const float LoadTime, const FString& MapName)
{
	UUECS3GameInstance::Instance->LevelManager->SetCurrentLoadCompletedLevel(MapName);
}

void UUECS3GameInstance::SetAllDropBoxTipsEffect(bool bIsDropTipsEffect)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UUECS3GameInstance::SetOtherPlayerMode~"));
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp==nullptr|| KbeApp->Entities()==nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUECS3GameInstance::SetAllDropBoxTipsEffect : KbeApp!"));
		return;
	}
	FString ModelNumber = TEXT("");
	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity && !Entity->IsPlayer() && !Entity->ClassName().Compare(FString("DropBox")))
		{
			if (ADropBoxCharacter* DropBox = Cast<ADropBoxCharacter>(Entity->Actor()))
			{
				if (bIsDropTipsEffect)
				{
					DropBox->SetBoxEffect();
				}
				else
				{
					DropBox->StopEffect();
				}
			}
		}
	}

}

bool UUECS3GameInstance::IsEnterGameBefor()
{
	class ALevelScriptActor* LevelScriptActor = UGolbalBPFunctionLibrary::GetMainLevelActor();
	if (LevelScriptActor)
	{
		ANewCreateRoleLevel *CreateRoleLevel = Cast<ANewCreateRoleLevel>(LevelScriptActor);
		ANewSelectRoleLevel *SelectRoleLevel = Cast<ANewSelectRoleLevel>(LevelScriptActor);
		ASelectCampLevel *SelectCampLevel = Cast<ASelectCampLevel>(LevelScriptActor);
		if (CreateRoleLevel || SelectRoleLevel || SelectCampLevel)
		{
			return true;
		}
	}
	return false;
}

void UUECS3GameInstance::TimeSynchronization(FString& ServerTime)
{
	int64 itime = FCString::Atoi64(*ServerTime);
	RecordServerTime = FDateTime::Now().GetTicks() - itime;
}

void UUECS3GameInstance::CheckApplicationActivation(bool bIsActive)
{
	if (this->bIsGameWindowActive == bIsActive)
	{
		return;
	}

	this->bIsGameWindowActive = bIsActive;

	//UI处理
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->CheckApplicationActivation(bIsActive);
	}

	//窗口切换激活状态调用逻辑
	if (IsValid(this->ControllerModeMgr))
	{
		if (bIsActive)
		{
			this->ControllerModeMgr->ChangeControlModeToActive(true);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnApplicationActivationStateChanged --- RecoveryMode"));
		}
		else
		{
			//游戏窗口为非激活模式
			this->ControllerModeMgr->ChangeControlModeToActive(false);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnApplicationActivationStateChanged --- ChangeMode"));
		}
	}
}

void UUECS3GameInstance::ClearObjectHandles(const void * UserObject)
{
	if (IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearAllTimersForObject(UserObject);
	}
	if (IsValid(UUECS3GameInstance::Instance->ResourceManager))
	{
		UUECS3GameInstance::Instance->ResourceManager->ReleaseHandlesByObject(UserObject);
	}
}

void UUECS3GameInstance::CheckLanderSystemSetting()
{
	FString ScreenPercentage;
	FString Resolution;
	FString IsFullScreenMode;
	FString IsVerticalSynchronization;
	FString CameraTurnSpeed;
	FString CameraMaxArmLen;
	FString WideAngle;
	FString MainVolumeInfo;
	FString BGMVolume;
	FString VoiceVolume;
	FString EffectVolume;

	FParse::Value(FCommandLine::Get(), TEXT("ScreenPercentage="), ScreenPercentage);
	FParse::Value(FCommandLine::Get(), TEXT("Resolution="), Resolution);
	FParse::Value(FCommandLine::Get(), TEXT("IsFullScreenMode="), IsFullScreenMode);
	FParse::Value(FCommandLine::Get(), TEXT("IsVerticalSynchronization="), IsVerticalSynchronization);
	FParse::Value(FCommandLine::Get(), TEXT("MouseSensitivity="), CameraTurnSpeed);
	FParse::Value(FCommandLine::Get(), TEXT("LenDist="), CameraMaxArmLen);
	FParse::Value(FCommandLine::Get(), TEXT("WideAngle="), WideAngle);
	FParse::Value(FCommandLine::Get(), TEXT("MainVolumeInfo="), MainVolumeInfo);
	FParse::Value(FCommandLine::Get(), TEXT("MusicInfo="), BGMVolume);
	FParse::Value(FCommandLine::Get(), TEXT("SoundInfo="), EffectVolume);
	FParse::Value(FCommandLine::Get(), TEXT("AudioInfo="), VoiceVolume);

	if (!ScreenPercentage.IsEmpty())
	{
		ULocalUserSettingData* LocalUserSettingData = LocalDataSaveManager->LocalUserSettingData;
		bool InitLocalUserSettingData = false;
		if (!LocalDataSaveManager->DeosLocalUserSettingDataExist())
		{
			LocalUserSettingData->InitLocalUserSettingData();
			InitLocalUserSettingData = true;
		}
		LocalUserSettingData->VideoSettingData.ScreenPercentage = FSTRING_TO_INT(ScreenPercentage);
		LocalUserSettingData->VideoSettingData.Resolution = Resolution;
		LocalUserSettingData->VideoSettingData.IsFullScreenMode = FSTRING_TO_INT(IsFullScreenMode) == 0 ? false : true;
		LocalUserSettingData->VideoSettingData.IsVerticalSynchronization = FSTRING_TO_INT(IsVerticalSynchronization) == 0 ? false : true;
		LocalUserSettingData->SetVideoSetting(FSTRING_TO_FLOAT(CameraTurnSpeed) / 100.0f, FSTRING_TO_FLOAT(CameraMaxArmLen) / 100.0f, FSTRING_TO_FLOAT(WideAngle) / 100.0f);

		TArray<FString> MainVolumeInfos = UGolbalBPFunctionLibrary::SplitString(MainVolumeInfo, false, ":");
		if (MainVolumeInfos.Num() > 1)
		{
			LocalUserSettingData->SoundSettingData.IsMainVolumeOff = FSTRING_TO_INT(MainVolumeInfos[1]) == 0 ? false : true;
			LocalUserSettingData->SoundSettingData.MainVolume = FSTRING_TO_FLOAT(MainVolumeInfos[0]) / 100.0f;
		}

		TArray<FString> BGMVolumeInfos = UGolbalBPFunctionLibrary::SplitString(BGMVolume, false, ":");
		if (BGMVolumeInfos.Num() > 1)
		{
			LocalUserSettingData->SoundSettingData.IsBGMVolumeOff = FSTRING_TO_INT(BGMVolumeInfos[1]) == 0 ? false : true;
			LocalUserSettingData->SoundSettingData.BGMVolume = FSTRING_TO_FLOAT(BGMVolumeInfos[0]) / 100.0f;
		}
		TArray<FString> VoiceVolumeInfos = UGolbalBPFunctionLibrary::SplitString(VoiceVolume, false, ":");
		if (VoiceVolumeInfos.Num() > 1)
		{
			LocalUserSettingData->SoundSettingData.IsVoiceVolumeOff = FSTRING_TO_INT(VoiceVolumeInfos[1]) == 0 ? false : true;
			LocalUserSettingData->SoundSettingData.VoiceVolume = FSTRING_TO_FLOAT(VoiceVolumeInfos[0]) / 100.0f;
		}
		TArray<FString> EffectVolumeInfos = UGolbalBPFunctionLibrary::SplitString(EffectVolume, false, ":");
		if (EffectVolumeInfos.Num() > 1)
		{
			LocalUserSettingData->SoundSettingData.IsEffectVolumeOff = FSTRING_TO_INT(EffectVolumeInfos[1]) == 0 ? false : true;
			LocalUserSettingData->SoundSettingData.EffectVolume = FSTRING_TO_FLOAT(EffectVolumeInfos[0]) / 100.0f;
		}

		if (InitLocalUserSettingData)
		{
			LocalDataSaveManager->SaveLocalUserSettingDataFile();
		}
		else
		{
			LocalUserSettingData->SaveVideoDataToFile(LocalUserSettingData->VideoSettingData);
			LocalUserSettingData->SaveSoundDataToFile(LocalUserSettingData->SoundSettingData);
		}
	}
}

void UUECS3GameInstance::OnActorEndPlay(AActor* Actor, EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		ClearObjectHandles(Actor);
		if (IsValid(Actor))
		{
			Actor->OnEndPlay.RemoveDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
		}
	}
}

// Fill out your copyright notice in the Description page of Project Settings.

#include "LocalUserSettingData.h"
#include "Chuangshi.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/Role/RoleRelationInterface.h"
#include "Interface/Role/RoleTongInterface.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Manager/GameStatus.h"
#include "Manager/AudioManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/CfgManager.h"
#include "Manager/ResourceManager.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/LocalDataSaveManager.h"
#include "Util/CS3Debug.h"
#include "Kismet/KismetMathLibrary.h"
#include <winbase.h>


CONTROL_COMPILE_OPTIMIZE_START

const FString& ULocalUserSettingData::GetFileName()
{
	return FileName;
}

void ULocalUserSettingData::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		if (IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearAllTimersForObject(this);
		}
		if (IsValid(UUECS3GameInstance::Instance->ResourceManager))
		{
			UUECS3GameInstance::Instance->ResourceManager->ReleaseHandlesByObject(this);
		}
	}
	Super::BeginDestroy();
}

void ULocalUserSettingData::InitLocalUserSettingData()
{
	DefaultVideoDataToFile();
	DefaultCustomDataToFile();
	DefaultSoundDataToFile();
	DefaultBaseDataToFile();
	DefaultUIShowDataToFile();
	DefaultQuickBarDataToFile();
	DefaultCombatDataToFile();
	DefaultAllShortcutKeyDataToFile();
}

const FSYSTEM_DEFAULT_DATA* ULocalUserSettingData::GetDefaultSystemData()
{	
	if ((!IsValid(UUECS3GameInstance::Instance)) || (!IsValid(UUECS3GameInstance::Instance->CfgManager)))return nullptr;
	FString RowId = TEXT("1");
	const FSYSTEM_DEFAULT_DATA* SystemData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_SYSTEM_DEFAULT_DATA)->GetRow<FSYSTEM_DEFAULT_DATA>(RowId);
	if (!SystemData) CS3_Warning(TEXT("GetDefaultSystemData is not found~"));

	return SystemData;
}

void ULocalUserSettingData::GetCameraArmLenDataByCfg(float& CameraArmLenMax, float& CameraArmLenMin)
{
	FVIDEOSETTING_RANGEVALUE_DATA RangeValueVideoData = GetRangeValueVideoData();

	if (RangeValueVideoData.CameraArmLenMax.Num() == 1)
	{
		CameraArmLenMax = RangeValueVideoData.CameraArmLenMax[0];
	}
	else if (RangeValueVideoData.CameraArmLenMax.Num() >= VideoSettingData.ScreenPercentage && RangeValueVideoData.CameraArmLenMax.Num() > 0)
	{
		CameraArmLenMax = RangeValueVideoData.CameraArmLenMax[VideoSettingData.ScreenPercentage];
	}
	else
	{
		CameraArmLenMax = 2500.0f;
	}

	if (RangeValueVideoData.CameraArmLenMin.Num() == 1)
	{
		CameraArmLenMin = RangeValueVideoData.CameraArmLenMin[0];
	}
	else if (RangeValueVideoData.CameraArmLenMin.Num() >= VideoSettingData.ScreenPercentage && RangeValueVideoData.CameraArmLenMin.Num() > 0)
	{
		CameraArmLenMin = RangeValueVideoData.CameraArmLenMin[VideoSettingData.ScreenPercentage];
	}
	else
	{
		CameraArmLenMin = -100.0f;
	}
}

void ULocalUserSettingData::GetCameraArmLenData(float & CameraArmLenMax, float & CameraArmLenMin)
{
	FVIDEOSETTING_RANGEVALUE_DATA RangeValueVideoData = GetRangeValueVideoData();

	CameraArmLenMax = VideoSettingData.CameraMaxArmLen;

	if (RangeValueVideoData.CameraArmLenMin.Num() == 1)
	{
		CameraArmLenMin = RangeValueVideoData.CameraArmLenMin[0];
	}
	else if (RangeValueVideoData.CameraArmLenMin.Num() >= VideoSettingData.ScreenPercentage && RangeValueVideoData.CameraArmLenMin.Num() > 0)
	{
		CameraArmLenMin = RangeValueVideoData.CameraArmLenMin[VideoSettingData.ScreenPercentage];
	}
	else
	{
		CameraArmLenMin = -100.0f;
	}
}

void ULocalUserSettingData::SetPlayerCameraSocketOffset()
{
	//需InWord才能设置
	UGameStatus* GameState = UUECS3GameInstance::Instance->GameStatus;
	if ((GameState && GameState->IsCurrStatus(EGameStatus::InWorld)))
	{
		APlayerCharacter* player = (APlayerCharacter*)UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
		if (player)
		{
			UGolbalBPFunctionLibrary::SetCameraFOV(player->CameraComponent, VideoSettingData.WideAngle);
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(player->SpringArmCompent, FVector(-1.0f*(VideoSettingData.CameraMaxLen), 0.0f, 0.0f));
			UGolbalBPFunctionLibrary::SetCameraTargetArmLength(player->SpringArmCompent, VideoSettingData.CameraMaxArmLen);
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("ApplySettingVideoSettingData  VideoSettingData.CameraMaxLen  ==%f   VideoSettingData.WideAngle=%d VideoSettingData.CameraMaxArmLen=%f"), VideoSettingData.CameraMaxLen, VideoSettingData.WideAngle, VideoSettingData.CameraMaxArmLen);
		}
	}
}

FVIDEOSETTING_RANGEVALUE_DATA ULocalUserSettingData::GetRangeValueVideoData()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();

	if (nullptr == SystemData)return FVIDEOSETTING_RANGEVALUE_DATA();

	return SystemData->RangeValueVideoData;
}

void ULocalUserSettingData::DefaultVideoDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		VideoSettingData = SystemData->VideoData;
	}
	else
	{
		VideoSettingData.ScreenPercentage = 3;
		VideoSettingData.Resolution = "1600x900";
		VideoSettingData.IsFullScreenMode = false;
		VideoSettingData.IsVerticalSynchronization = false;
		VideoSettingData.IsCharacterMode = false;
		VideoSettingData.CameraMaxLen = 300.0f;
		VideoSettingData.WideAngle = 90.0f;
		VideoSettingData.UIScale = 1.0f;
		VideoSettingData.CameraTurnSpeed = 1.f;
		VideoSettingData.CameraMaxArmLen = 1000.0f;
	}
	ApplyCustomWindowResolution();
}

void ULocalUserSettingData::DefaultCustomDataToFile()
{
	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const FCUSTOMSETTING_DATA* Data = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_DEFAULT_COSTOM)->GetRow<FCUSTOMSETTING_DATA>(FString::FromInt(VideoSettingData.ScreenPercentage));

	if (Data)
	{
		CustomSettingData.AntiAliasingQuality = Data->AntiAliasingQuality;
		CustomSettingData.ScreenRoleNum = Data->ScreenRoleNum;
		CustomSettingData.ScreenEffectNum = Data->ScreenEffectNum;
		CustomSettingData.IsWeatherEffect = Data->IsWeatherEffect;
		CustomSettingData.IsShieldRainAndSnow = Data->IsShieldRainAndSnow;
		CustomSettingData.IsGroundSurfaceDetail = Data->IsGroundSurfaceDetail;
		CustomSettingData.IsGrassAnimation = Data->IsGrassAnimation;
		CustomSettingData.IsTransparentBlendRendering = Data->IsTransparentBlendRendering;
		CustomSettingData.IsVegetationInteraction = Data->IsVegetationInteraction;
		CustomSettingData.IsFullScreenFloodlight = Data->IsFullScreenFloodlight;
		CustomSettingData.IsSurfaceFloodlight = Data->IsSurfaceFloodlight;
		CustomSettingData.IsCloudShadow = Data->IsCloudShadow;
		CustomSettingData.IsRealtimeShadow = Data->IsRealtimeShadow;
		CustomSettingData.IsAtomizationEffect = Data->IsAtomizationEffect;
		CustomSettingData.WaterSurfaceAccuracy = Data->WaterSurfaceAccuracy;
		CustomSettingData.LongRangeDisplay = Data->LongRangeDisplay;
		CustomSettingData.VegetationAccuracy = Data->VegetationAccuracy;
		CustomSettingData.TextureFiltering = Data->TextureFiltering;
		CustomSettingData.ShadowQuality = Data->ShadowQuality;
		CustomSettingData.GroundSurfaceAccuracy = Data->GroundSurfaceAccuracy;
	}
}

void ULocalUserSettingData::DefaultSoundDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		SoundSettingData = SystemData->SoundData;
	}
	else
	{
		SoundSettingData.IsMainVolumeOff = false;
		SoundSettingData.MainVolume = 1.0f;
		SoundSettingData.IsBGMVolumeOff = false;
		SoundSettingData.BGMVolume = 1.0f;
		SoundSettingData.IsEffectVolumeOff = false;
		SoundSettingData.EffectVolume = 1.0f;
		SoundSettingData.IsVoiceVolumeOff = false;
		SoundSettingData.VoiceVolume = 1.0f;
	}	
}

void ULocalUserSettingData::DefaultBaseDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		BaseSettingData = SystemData->BaseData;
	}
	else
	{
		BaseSettingData.IsDropTipsEffect = true;
		BaseSettingData.IsShieldSystemTips = false;
		BaseSettingData.IsCloseEnterStoryMode = false;
		BaseSettingData.IsShowTeammate = true;
		BaseSettingData.IsShowNPC = true;
		BaseSettingData.IsShowMonster = true;
		BaseSettingData.IsOpenHelp = true;
		BaseSettingData.IsShowOnlineRemind = false;
		BaseSettingData.IsAutoPickUpAll = false;
		BaseSettingData.IsAutoTrackingQuest = true;
		BaseSettingData.IsMousePickUp = true;
		BaseSettingData.IsOpenGetEquipTips = true;
		BaseSettingData.IsAutoShowSpell = false;
	}	
}

void ULocalUserSettingData::DefaultUIShowDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		UIShowSettingData = SystemData->UIShowData;
	}
	else
	{
		UIShowSettingData.IsShowOtherPlayerName = true;
		UIShowSettingData.IsShowOtherPlayerTitle = true;
		UIShowSettingData.IsShowNPCName = true;
		UIShowSettingData.IsShowNPCTitle = true;
		UIShowSettingData.IsShowSelfName = false;
		UIShowSettingData.IsShowSelfTitle = false;
		UIShowSettingData.IsShowMagicPetName = false;
		UIShowSettingData.IsShowOtherPlayerBloodBar = true;
		UIShowSettingData.IsShowNPCBloodBar = true;
		UIShowSettingData.IsShowSelfBloodBar = false;
		UIShowSettingData.IsShowMagicPetBloodBar = false;
		UIShowSettingData.IsShowOtherPlayerGangName = true;
		UIShowSettingData.IsShowSelfGangName = false;
		UIShowSettingData.IsShowPlayerTalkBox = true;
		UIShowSettingData.IsShowNPCTalkBox = true;
		UIShowSettingData.IsShowTargetTarget = true;
		UIShowSettingData.IsShowProgressOfTeammateQuest = true;
	}
}

void ULocalUserSettingData::DefaultQuickBarDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		QuickBarSettingData = SystemData->QuickBaseData;
	}
	else
	{
		QuickBarSettingData.IsSkillTrack = true;
		QuickBarSettingData.IsSkillSmart = false;
		QuickBarSettingData.IsShowSideBar1 = false;
		QuickBarSettingData.IsShowSideBar2 = false;
		QuickBarSettingData.IsShowSideBar3 = false;
		QuickBarSettingData.IsShowSideBar4 = false;
		QuickBarSettingData.IsShowSideBar5 = false;
		QuickBarSettingData.IsShowExpandBar1 = false;
		QuickBarSettingData.IsShowExpandBar2 = false;
		QuickBarSettingData.IsShowExpandBar3 = false;
		QuickBarSettingData.IsShowExpandBar4 = false;
		QuickBarSettingData.IsShowExpandBar5 = false;
		QuickBarSettingData.IsShowExpandBar6 = false;
	}
}

void ULocalUserSettingData::DefaultCombatDataToFile()
{
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		CombatSettingData = SystemData->CombatData;
	}
	else
	{
		CombatSettingData.IsRecommendMode = true;
		CombatSettingData.IsACTMode = false;
		CombatSettingData.IsAutoFightBack = true;
		CombatSettingData.IsShowPlayerSkillName = true;
		CombatSettingData.IsShowTargetStateInfo = true;
		CombatSettingData.IsShowTargetDamage = true;
		CombatSettingData.IsShowTargetSkillName = true;
		CombatSettingData.IsShowPlayerStateInfo = true;
		CombatSettingData.IsShowPlayerDamage = true;
	}
}

void ULocalUserSettingData::DefaultAllShortcutKeyDataToFile()
{

}

void ULocalUserSettingData::DefaultShortcutKeyDataToFile(SHORTCUTKEY_TYPE_ENUM KeyType)
{

}

void ULocalUserSettingData::SaveVideoDataToFile(FVIDEOSETTING_DATA data)
{
	VideoSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
	SaveVideoDataToLauncherRecordIniFile(data);
}

void ULocalUserSettingData::SaveVideoDataToLauncherRecordIniFile(FVIDEOSETTING_DATA data)
{
	FString ProfilePath;
#if WITH_EDITOR
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/Windows/launcherRecord.ini");
#else
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/WindowsNoEditor/launcherRecord.ini");
#endif
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

	//全屏模式
	FString IsFullScreenMode = data.IsFullScreenMode == false ? TEXT("0") : TEXT("1");
	// 垂直同步
	FString IsVerticalSynchronization = data.IsVerticalSynchronization == false ? TEXT("0") : TEXT("1");
	//人物同模
	FString CharacterMode = data.IsCharacterMode == false ? TEXT("0") : TEXT("1");
	//游戏分辨率
	FString Resolution = data.Resolution;
	//画质
	FString ScreenPercentage = INT_TO_FSTRING(data.ScreenPercentage);

	FVIDEOSETTING_RANGEVALUE_DATA  RangeValueVideoData = GetRangeValueVideoData();
	float WideAnglePercent = UKismetMathLibrary::MapRangeUnclamped(data.WideAngle, RangeValueVideoData.WideAngleMin, RangeValueVideoData.WideAngleMax, 0.0f, 1.0f);
	float CameraTurnSpeedPercent = UKismetMathLibrary::MapRangeUnclamped(data.CameraTurnSpeed, RangeValueVideoData.CameraTurnSpeedMin, RangeValueVideoData.CameraTurnSpeedMax, 0.0f, 1.0f);
	float CameraArmLenMin, CameraArmLenMax;
	GetCameraArmLenDataByCfg(CameraArmLenMax, CameraArmLenMin);
	float CameraMaxArmLenPercent = UKismetMathLibrary::MapRangeUnclamped(data.CameraMaxArmLen, CameraArmLenMin, CameraArmLenMax, 0.0f, 1.0f);

	//镜头距离，数值为0--100；
	FString LenDist = INT_TO_FSTRING(CameraMaxArmLenPercent * 100);
	//鼠标灵敏度，数值为0--100；
	FString MouseSensitivity = INT_TO_FSTRING(CameraTurnSpeedPercent * 100);
	// 广角，数值为0--100；
	FString WideAngle = INT_TO_FSTRING(WideAnglePercent * 100);

	WritePrivateProfileString(TEXT("GameSetting"), TEXT("IsFullScreenMode"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(IsFullScreenMode)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("IsVerticalSynchronization"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(IsVerticalSynchronization)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("CharacterMode"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(CharacterMode)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("Resolution"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(Resolution)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("ScreenPercentage"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ScreenPercentage)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("LenDist"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(LenDist)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("MouseSensitivity"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(MouseSensitivity)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("WideAngle"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(WideAngle)), FilePath);
}

void ULocalUserSettingData::SaveCustomDataToFile(FCUSTOMSETTING_DATA data)
{
	CustomSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
}

void ULocalUserSettingData::SaveSoundDataToFile(FSOUNDSETTING_DATA data)
{
	SoundSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
	SaveSoundDataToLauncherRecordIniFile(data);
}

void ULocalUserSettingData::SaveSoundDataToLauncherRecordIniFile(FSOUNDSETTING_DATA data)
{
	FString ProfilePath;
#if WITH_EDITOR
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/Windows/launcherRecord.ini");
#else
	ProfilePath = FPaths::ProjectSavedDir() + TEXT("Config/WindowsNoEditor/launcherRecord.ini");
#endif
	ProfilePath.ReplaceInline(TEXT("/"), TEXT("\\"), ESearchCase::CaseSensitive);
	LPCTSTR FilePath = TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(ProfilePath));

	FString IsMainVolumeOff = data.IsMainVolumeOff == false ? TEXT("0") : TEXT("1");
	FString IsBGMVolumeOff = data.IsBGMVolumeOff == false ? TEXT("0") : TEXT("1");
	FString IsEffectVolumeOff = data.IsEffectVolumeOff == false ? TEXT("0") : TEXT("1");
	FString IsVoiceVolumeOff = data.IsVoiceVolumeOff == false ? TEXT("0") : TEXT("1");
	//主音量
	FString MainVolumeInfo = FLOAT_TO_FSTRING(data.MainVolume * 100) + TEXT(":") + IsMainVolumeOff;
	//背景音量
	FString MusicInfo = FLOAT_TO_FSTRING(data.BGMVolume * 100) + TEXT(":") + IsBGMVolumeOff;
	//语音音量
	FString AudioInfo = FLOAT_TO_FSTRING(data.VoiceVolume * 100) + TEXT(":") + IsVoiceVolumeOff;
	//音效音量
	FString SoundInfo = FLOAT_TO_FSTRING(data.EffectVolume * 100) + TEXT(":") + IsEffectVolumeOff;

	WritePrivateProfileString(TEXT("GameSetting"), TEXT("MainVolumeInfo"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(MainVolumeInfo)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("MusicInfo"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(MusicInfo)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("AudioInfo"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(AudioInfo)), FilePath);
	WritePrivateProfileString(TEXT("GameSetting"), TEXT("SoundInfo"), TCHAR_TO_WCHAR(FSTRING_TO_TCHAR(SoundInfo)), FilePath);
}

void ULocalUserSettingData::SaveBaseDataToFile(FBASESETTING_DATA data)
{
	BaseSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
}

void ULocalUserSettingData::SaveUIShowDataToFile(FUISHOWSETTING_DATA data)
{
	UIShowSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
}

void ULocalUserSettingData::SaveQuickBarDataToFile(FQUICKBAESETTING_DATA data)
{
	QuickBarSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
}

void ULocalUserSettingData::SaveCombatDataToFile(FCOMBATSETTING_DATA data)
{
	CombatSettingData = data;
	UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
}

void ULocalUserSettingData::ApplyCustomWindowResolution()
{
	FString CustomWindowResolution = UUECS3GameInstance::Instance->GameDefault->CustomWindowResolution;
	if (!CustomWindowResolution.IsEmpty())
	{
		TArray<FString> resolutionString = UGolbalBPFunctionLibrary::SplitString(CustomWindowResolution, false, TEXT("x"));
		if (resolutionString.Num() == 2)
		{
			bool isNeedSetResolution = true;
			for (auto value : resolutionString)
			{
				if (!value.IsNumeric())
				{
					isNeedSetResolution = false;
				}
			}
			if (isNeedSetResolution)
			{
				VideoSettingData.Resolution = CustomWindowResolution;
				UGolbalBPFunctionLibrary::GameInstance()->LocalDataSaveManager->SaveLocalUserSettingDataFile();
				SaveVideoDataToLauncherRecordIniFile(VideoSettingData);
			}
		}
	}
}

void ULocalUserSettingData::ApplySystemSettingData()
{	
	ApplyCustomWindowResolution();
	ApplySettingVideoSettingData();
	//ApplySettingCustomData();
	ApplySoundSettingData();
	ApplyBaseSettingData();
	ApplyUIShowSettingData();
	ApplyQuickBarSettingData();
	ApplyCombatSettingData();
}

void ULocalUserSettingData::ApplySettingVideoSettingData_Implementation()
{
	TArray<int> ScreenPercentages = { 75,85,100,200 };
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		ScreenPercentages = SystemData->RangeValueVideoData.ScreenPercentages;
	}

	UWorld* world = UUECS3GameInstance::Instance->GetWorld();
	FString mode = "w";
	FString cmd = "";
	FString Resolution = VideoSettingData.Resolution;

	if (ScreenPercentages.Num() > VideoSettingData.ScreenPercentage)
	{
		cmd = TEXT("r.ScreenPercentage ") + INT_TO_FSTRING(ScreenPercentages[VideoSettingData.ScreenPercentage]);
		UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ApplySettingVideoSettingData   r.ScreenPercentage  ==%s "), *cmd);
	}

	if (VideoSettingData.IsFullScreenMode)
	{
		if (UUECS3GameInstance::Instance->GetWorld()->WorldType == EWorldType::PIE)
		{
			mode = TEXT("wf");
		}
		else
		{
			mode = TEXT("f");
		}
	}

	cmd = TEXT("r.SetRes ") + Resolution + mode;
	UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ApplySettingVideoSettingData   r.SetRes   ==%s "), *cmd);
	///设置垂直同步
	FString VSync = TEXT("r.VSync ");
#if WITH_EDITOR
	VSync = TEXT("r.VSyncEditor ");
#endif
	cmd = VSync + INT_TO_FSTRING(VideoSettingData.IsVerticalSynchronization);
	UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
	
	SetPlayerCameraSocketOffset();
	ApplyScreenPercentagesRender();

	OnVideoSettingChange.Broadcast(VideoSettingData);
}

void ULocalUserSettingData::ApplySettingCustomData()
{
	UWorld* world = UUECS3GameInstance::Instance->GetWorld();
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	int32 AntiAliasing = SystemData->AntiAliasingMethod.AntiAliasingMethod;
	///Close AntiAliasing
	if (CustomSettingData.AntiAliasingQuality == 0)
	{
		FString cmd = TEXT("r.DefaultFeature.AntiAliasing ") + INT_TO_FSTRING(0);
		UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
		return;
	}
	else
	{
		FString cmd = TEXT("r.DefaultFeature.AntiAliasing ") + INT_TO_FSTRING(AntiAliasing);
		UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
	}

	if (VideoSettingData.IsFullScreenMode)
	{
		if (CustomSettingData.AntiAliasingQuality > 2)
		{
			FString cmd = TEXT("sg.AntiAliasingQuality ") + INT_TO_FSTRING(CustomSettingData.AntiAliasingQuality - 1);
			UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
		}
	}
	else
	{
		FString cmd = TEXT("sg.AntiAliasingQuality ") + INT_TO_FSTRING(CustomSettingData.AntiAliasingQuality - 1);
		UKismetSystemLibrary::ExecuteConsoleCommand(world, cmd);
	}
}

void ULocalUserSettingData::ApplySoundSettingData()
{
	///主音量
	if (SoundSettingData.IsMainVolumeOff)
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetMasterVol(0.0f);
	}
	else
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetMasterVol(SoundSettingData.MainVolume);
	}
	///背景音量
	if (SoundSettingData.IsBGMVolumeOff)
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetBgVol(0.0f);
	}
	else
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetBgVol(SoundSettingData.BGMVolume);
	}
	///音效音量
	if (SoundSettingData.IsEffectVolumeOff)
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetEffVol(0.0f);
		UGolbalBPFunctionLibrary::AudioManager()->SetBgEffVol(0.0f);
	}
	else
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetEffVol(SoundSettingData.EffectVolume);
		UGolbalBPFunctionLibrary::AudioManager()->SetBgEffVol(SoundSettingData.EffectVolume);
	}
	///语音音量
	if (SoundSettingData.IsVoiceVolumeOff)
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetVoiceVol(0.0f);
	}
	else
	{
		UGolbalBPFunctionLibrary::AudioManager()->SetVoiceVol(SoundSettingData.VoiceVolume);
	}
}

float ULocalUserSettingData::GetMainVolume()
{
	if (SoundSettingData.IsMainVolumeOff)
	{
		return 0.0f;
	}
	return SoundSettingData.MainVolume;

}

float ULocalUserSettingData::GetBgVol()
{
	if (SoundSettingData.IsBGMVolumeOff)
	{
		return 0.0f;
	}
	return SoundSettingData.BGMVolume* GetMainVolume();
}

float ULocalUserSettingData::GetVoiceVol()
{
	if (SoundSettingData.IsVoiceVolumeOff)
	{
		return 0.0f;
	}
	return SoundSettingData.VoiceVolume* GetMainVolume();
}

float ULocalUserSettingData::GetEffVol()
{
	if (SoundSettingData.IsEffectVolumeOff)
	{
		return 0.0f;
	}
	return SoundSettingData.EffectVolume* GetMainVolume();
}

void ULocalUserSettingData::IsValidVideoData()
{
	float CameraLenMax = -100.0f;
	float CameraLenMin = -300.0f;
	float CameraArmLenMax = 2500.0f;
	float CameraArmLenMin = -100.0f;
	float DefaultCameraLen = -300.0f;
	float DefaultCameraArmLen = 1000.0f;
	float CameraTurnSpeedMax = 1.5f;
	float CameraTurnSpeedMin = 0.5f;
	float DefaultCameraTurnSpeed = 1.0f;
	float WideAngleMax = 90.0f;
	float WideAngleMin = 60.0f;
	float DefaultWideAngle = 90.0f;

	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	if (SystemData)
	{
		CameraLenMax = SystemData->RangeValueVideoData.CameraLenMax;
		CameraLenMin= SystemData->RangeValueVideoData.CameraLenMin;
		DefaultCameraLen = SystemData->VideoData.CameraMaxLen;
		GetCameraArmLenDataByCfg(CameraArmLenMax, CameraArmLenMin);
		
		DefaultCameraArmLen = SystemData->VideoData.CameraMaxArmLen;
		CameraTurnSpeedMax = SystemData->RangeValueVideoData.CameraTurnSpeedMax;
		CameraTurnSpeedMin = SystemData->RangeValueVideoData.CameraTurnSpeedMin;
		DefaultCameraTurnSpeed = SystemData->VideoData.CameraTurnSpeed;

		WideAngleMax = SystemData->RangeValueVideoData.WideAngleMax;
		WideAngleMin = SystemData->RangeValueVideoData.WideAngleMin;
		DefaultWideAngle = SystemData->VideoData.WideAngle;
	}

	bool bIsValidData = true;
	if (VideoSettingData.ScreenPercentage > 3 || VideoSettingData.ScreenPercentage < 0)
	{
		VideoSettingData.ScreenPercentage = 3;
		bIsValidData = false;
	}
	if (VideoSettingData.CameraMaxLen > CameraLenMax || VideoSettingData.CameraMaxLen < CameraLenMin)
	{
		VideoSettingData.CameraMaxLen = DefaultCameraLen;
		bIsValidData = false;
	}
	if (VideoSettingData.CameraMaxArmLen > CameraArmLenMax || VideoSettingData.CameraMaxArmLen < CameraArmLenMin)
	{
		VideoSettingData.CameraMaxArmLen = DefaultCameraArmLen;
		bIsValidData = false;
	}
	if (VideoSettingData.WideAngle > WideAngleMax || VideoSettingData.WideAngle < WideAngleMin)
	{
		VideoSettingData.WideAngle = DefaultWideAngle;
		bIsValidData = false;
	}
	if (VideoSettingData.CameraTurnSpeed > CameraTurnSpeedMax || VideoSettingData.CameraTurnSpeed < CameraTurnSpeedMin)
	{
		VideoSettingData.CameraTurnSpeed = DefaultCameraTurnSpeed;
		bIsValidData = false;
	}
}

void ULocalUserSettingData::SaveVideoSettingDataToConfig()
{
	if (GConfig == nullptr)return;

	if (VideoSettingData.IsFullScreenMode)
	{
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("FullscreenMode"), 1, GGameUserSettingsIni);
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("LastConfirmedFullscreenMode"), 1, GGameUserSettingsIni);
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("PreferredFullscreenMode"), 1, GGameUserSettingsIni);
	}
	else
	{
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("FullscreenMode"), 2, GGameUserSettingsIni);
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("LastConfirmedFullscreenMode"), 2, GGameUserSettingsIni);
		GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("PreferredFullscreenMode"), 2, GGameUserSettingsIni);
	}
	TArray<FString> ResolutionValue = UGolbalBPFunctionLibrary::SplitString(VideoSettingData.Resolution, false, TEXT("x"));
	if (ResolutionValue.Num() >= 2)
	{
		FIntPoint Resolution;
		Resolution.X = FSTRING_TO_INT(ResolutionValue[0]);
		Resolution.Y = FSTRING_TO_INT(ResolutionValue[1]);
		if (Resolution.X > 0 && Resolution.Y > 0)
		{
			GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("ResolutionSizeX"), Resolution.X, GGameUserSettingsIni);
			GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("ResolutionSizeY"), Resolution.Y, GGameUserSettingsIni);
			GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("LastUserConfirmedResolutionSizeX"), Resolution.X, GGameUserSettingsIni);
			GConfig->SetInt(TEXT("/Script/Engine.GameUserSettings"), TEXT("LastUserConfirmedResolutionSizeY"), Resolution.Y, GGameUserSettingsIni);
		}		
	}
	GConfig->Flush(false, GGameUserSettingsIni);
	///SaveConfig(CPF_Config,*GGameUserSettingsIni);
	const FSYSTEM_DEFAULT_DATA* SystemData = GetDefaultSystemData();
	int32 AntiAliasing = SystemData->AntiAliasingMethod.AntiAliasingMethod;
	///Close AntiAliasing
	if (CustomSettingData.AntiAliasingQuality==0)
	{
		AntiAliasing = 0;
	}
	GConfig->SetInt(TEXT("/Script/Engine.RendererSettings"), TEXT("r.DefaultFeature.AntiAliasing"), AntiAliasing, GEngineIni);
	GConfig->Flush(false, GEngineIni);
	ClearTimerHandle();
}

void ULocalUserSettingData::SetVideoSetting(float CameraTurnSpeed, float CameraMaxArmLen, float WideAngle)
{
	FVIDEOSETTING_RANGEVALUE_DATA  RangeValueVideoData = GetRangeValueVideoData();
	VideoSettingData.WideAngle = UKismetMathLibrary::MapRangeUnclamped(WideAngle, 0.0f, 1.0f, RangeValueVideoData.WideAngleMin, RangeValueVideoData.WideAngleMax);
	VideoSettingData.CameraTurnSpeed = UKismetMathLibrary::MapRangeUnclamped(CameraTurnSpeed, 0.0f, 1.0f, RangeValueVideoData.CameraTurnSpeedMin, RangeValueVideoData.CameraTurnSpeedMax);
	float CameraArmLenMin, CameraArmLenMax;
	GetCameraArmLenDataByCfg(CameraArmLenMax, CameraArmLenMin);
	VideoSettingData.CameraMaxArmLen = UKismetMathLibrary::MapRangeUnclamped(CameraMaxArmLen, 0.0f, 1.0f, CameraArmLenMin, CameraArmLenMax);
}

void ULocalUserSettingData::ApplyScreenPercentagesRender()
{	
	RenderCmds.Reset();
	FVIDEOSETTING_RANGEVALUE_DATA RangeValueVideoData = GetRangeValueVideoData();
	///根据不同分辨率获取对应设置
	FSCREENPERCENTAGES_RENDER_DATA ScreenPercentagesRender;
	if (RangeValueVideoData.ScreenPercentagesRender.Num()> VideoSettingData.ScreenPercentage)
	{
		ScreenPercentagesRender = RangeValueVideoData.ScreenPercentagesRender[VideoSettingData.ScreenPercentage];
	}
	
	///后处理抗锯齿
	FString cmd = TEXT("r.PostProcessAAQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.PostProcessAAQuality);
	RenderCmds.Add(cmd);

	
	///可视距离
	cmd = TEXT("r.SkeletalMeshLODBias ") + INT_TO_FSTRING(ScreenPercentagesRender.SkeletalMeshLODBias);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.ViewDistanceScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.ViewDistanceScale);
	RenderCmds.Add(cmd);
	///阴影质量
	cmd = TEXT("r.LightFunctionQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.LightFunctionQuality);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.ShadowQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.ShadowQuality);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.CSM.MaxCascades ") + INT_TO_FSTRING(ScreenPercentagesRender.Shadow_CSM_MaxCascades);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.MaxResolution ") + INT_TO_FSTRING(ScreenPercentagesRender.Shadow_MaxResolution);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.MaxCSMResolution ") + INT_TO_FSTRING(ScreenPercentagesRender.Shadow_MaxCSMResolution);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.RadiusThreshold ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Shadow_RadiusThreshold);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.DistanceScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Shadow_DistanceScale);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.CSM.TransitionScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Shadow_CSM_TransitionScale);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.Shadow.PreShadowResolutionFactor ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Shadow_PreShadowResolutionFactor);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.DistanceFieldShadowing ") + INT_TO_FSTRING(ScreenPercentagesRender.DistanceFieldShadowing);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.DistanceFieldAO ") + INT_TO_FSTRING(ScreenPercentagesRender.DistanceFieldAO);
	RenderCmds.Add(cmd);
	cmd = TEXT("r.VolumetricFog ") + INT_TO_FSTRING(ScreenPercentagesRender.VolumetricFog);
	RenderCmds.Add(cmd);
	if (ScreenPercentagesRender.VolumetricFog)
	{
		cmd = TEXT("r.VolumetricFog.GridPixelSize ") + INT_TO_FSTRING(ScreenPercentagesRender.VolumetricFog_GridPixelSize);
		RenderCmds.Add(cmd);
		cmd = TEXT("r.VolumetricFog.GridSizeZ ") + INT_TO_FSTRING(ScreenPercentagesRender.VolumetricFog_GridSizeZ);
		RenderCmds.Add(cmd);
		cmd = TEXT("r.VolumetricFog.HistoryMissSupersampleCount ") + INT_TO_FSTRING(ScreenPercentagesRender.VolumetricFog_HistoryMissSupersampleCount);
		RenderCmds.Add(cmd);
	}
	cmd = TEXT("r.LightMaxDrawDistanceScale ") + INT_TO_FSTRING(ScreenPercentagesRender.LightMaxDrawDistanceScale);
	RenderCmds.Add(cmd);	

	///贴图质量
	cmd = TEXT("r.Streaming.MipBias ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Streaming_MipBias);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.MaxAnisotropy ") + INT_TO_FSTRING(ScreenPercentagesRender.MaxAnisotropy);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Streaming.LimitPoolSizeToVRAM ") + INT_TO_FSTRING(ScreenPercentagesRender.Streaming_LimitPoolSizeToVRAM);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Streaming.PoolSize ") + INT_TO_FSTRING(ScreenPercentagesRender.Streaming_PoolSize);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Streaming.MaxEffectiveScreenSize ") + INT_TO_FSTRING(ScreenPercentagesRender.Streaming_MaxEffectiveScreenSize);
	RenderCmds.Add(cmd);

	///特效质量
	cmd = TEXT("r.TranslucencyLightingVolumeDim ") + INT_TO_FSTRING(ScreenPercentagesRender.TranslucencyLightingVolumeDim);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.RefractionQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.RefractionQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SSR.Quality ") + INT_TO_FSTRING(ScreenPercentagesRender.SSR_Quality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SceneColorFormat ") + INT_TO_FSTRING(ScreenPercentagesRender.SceneColorFormat);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.DetailMode ") + INT_TO_FSTRING(ScreenPercentagesRender.DetailMode);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.TranslucencyVolumeBlur ") + INT_TO_FSTRING(ScreenPercentagesRender.TranslucencyVolumeBlur);
	RenderCmds.Add(cmd);

	///cmd = TEXT("r.MaterialQualityLevel ") + INT_TO_FSTRING(ScreenPercentagesRender.MaterialQualityLevel);
	///RenderCmds.Add(cmd);

	cmd = TEXT("r.SSS.Scale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.SSS_Scale);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SSS.SampleSet ") + INT_TO_FSTRING(ScreenPercentagesRender.SSS_SampleSet);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SSS.Quality ") + INT_TO_FSTRING(ScreenPercentagesRender.SSS_Quality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SSS.HalfRes ") + INT_TO_FSTRING(ScreenPercentagesRender.SSS_HalfRes);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.EmitterSpawnRateScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.EmitterSpawnRateScale);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.ParticleLightQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.ParticleLightQuality);
	RenderCmds.Add(cmd);
	///后处理质量
	cmd = TEXT("r.MotionBlurQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.MotionBlurQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.AmbientOcclusionMipLevelFactor ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.AmbientOcclusionMipLevelFactor);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.AmbientOcclusionMaxQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.AmbientOcclusionMaxQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.AmbientOcclusionLevels ") + INT_TO_FSTRING(ScreenPercentagesRender.AmbientOcclusionLevels);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.AmbientOcclusionRadiusScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.AmbientOcclusionRadiusScale);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.DepthOfFieldQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.DepthOfFieldQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.RenderTargetPoolMin ") + INT_TO_FSTRING(ScreenPercentagesRender.RenderTargetPoolMin);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.LensFlareQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.LensFlareQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.SceneColorFringeQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.SceneColorFringeQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.EyeAdaptationQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.EyeAdaptationQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.BloomQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.BloomQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.FastBlurThreshold ") + INT_TO_FSTRING(ScreenPercentagesRender.FastBlurThreshold);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Upscale.Quality ") + INT_TO_FSTRING(ScreenPercentagesRender.Upscale_Quality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Tonemapper.GrainQuantization ") + INT_TO_FSTRING(ScreenPercentagesRender.Tonemapper_GrainQuantization);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.LightShaftQuality ") + INT_TO_FSTRING(ScreenPercentagesRender.LightShaftQuality);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Filter.SizeScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Filter_SizeScale);
	RenderCmds.Add(cmd);

	cmd = TEXT("r.Tonemapper.Quality ") + INT_TO_FSTRING(ScreenPercentagesRender.Tonemapper_Quality);
	RenderCmds.Add(cmd);

	///植物质量
	cmd = TEXT("foliage.DensityScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Foliage_DensityScale);
	RenderCmds.Add(cmd);

	cmd = TEXT("grass.DensityScale ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Grass_DensityScale);
	RenderCmds.Add(cmd);

	///Panini投影
	///cmd = TEXT("r.Upscale.Panini.D ") + FLOAT_TO_FSTRING(ScreenPercentagesRender.Upscale_PaniniD);
	///RenderCmds.Add(cmd);

	///每一帧执行一条指令
	DelayExecuteCmds();
}

void ULocalUserSettingData::DelayExecuteCmds()
{
	UWorld* World = UUECS3GameInstance::Instance->GetWorld();
	if (World)
	{
		TWeakObjectPtr<ULocalUserSettingData> DelayThisPtr(this);
		World->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				ULocalUserSettingData* LocalUserSettingData = DelayThisPtr.Get();
				if (LocalUserSettingData->RenderCmds.Num() > 0)
				{
					UWorld* World2 = UUECS3GameInstance::Instance->GetWorld();
					if (World2)
					{
						UKismetSystemLibrary::ExecuteConsoleCommand(World2, LocalUserSettingData->RenderCmds[0]);
						LocalUserSettingData->RenderCmds.RemoveAt(0);

						CS3_Display(CS3DebugType::CL_Undefined, TEXT("LocalUserSettingData->RenderCmds.Num() %d"), LocalUserSettingData->RenderCmds.Num());
					}

					if (LocalUserSettingData->RenderCmds.Num())
					{
						LocalUserSettingData->DelayExecuteCmds();
					}
				}
			}
		}));
	}
}

void ULocalUserSettingData::ClearTimerHandle()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayHandle);
	}
}

void ULocalUserSettingData::ApplyQuickBarSettingData_Implementation()
{

}

void ULocalUserSettingData::ApplyCombatSettingData_Implementation()
{

}

void ULocalUserSettingData::ApplyBaseSettingData_Implementation()
{	///需InWord才能设置
	UGameStatus* GameState = UUECS3GameInstance::Instance->GameStatus;
	if ((GameState && GameState->IsCurrStatus(EGameStatus::InWorld)))
	{
		///掉落提示光效
		UUECS3GameInstance::Instance->SetAllDropBoxTipsEffect(BaseSettingData.IsDropTipsEffect);

		URoleRelationInterface * RelationInterface = Cast<URoleRelationInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleRelationInterface"), 0));
		if (RelationInterface)
		{
			RelationInterface->SetNoticeLine(BaseSettingData.IsShowOnlineRemind);
		}
		URoleTongInterface * TongInterface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), 0));
		if (TongInterface)
		{
			TongInterface->SetNoticeLine(BaseSettingData.IsShowOnlineRemind);
		}
	}
}

void ULocalUserSettingData::ApplyUIShowSettingData_Implementation()
{

}
CONTROL_COMPILE_OPTIMIZE_END
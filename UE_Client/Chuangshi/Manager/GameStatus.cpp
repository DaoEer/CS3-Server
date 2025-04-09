// Fill out your copyright notice in the Description page of Project Settings.


#include "Manager/GameStatus.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PlayerController.h"
#include "LoginManager.h"
#include "StoryManager.h"
#include "Util/CS3Debug.h"
#include "Entity/Role/CS3Role.h"
#include "CS3Base/UIManager.h"
#include "LevelManager.h"
#include "AudioManager.h"
#include "MapManager.h"
#include "CharacterRideManager.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "MediaPlayerManager.h"
#include "CS3Base/BaseWindow.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/AtkStateMar.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include"Chuangshi.h"

CONTROL_COMPILE_OPTIMIZE_START

UGameStatus::UGameStatus()
{
	CurrStatus = EGameStatus::Login;
	LastStatus = EGameStatus::Login;
}
UGameStatus::~UGameStatus()
{
}

UGameStatus* UGameStatus::GetInstance()
{
	cs3_checkNoReentry();

	return (UGameStatus *)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_GameStatus")));
}

bool UGameStatus::IsCurrStatus(EGameStatus status)
{
	return CurrStatus == status;
}

bool UGameStatus::CheckChangeStatus(EGameStatus InStatus)
{
	if (InStatus == EGameStatus::InWorld)
	{
		if (!(UUECS3GameInstance::Instance->LoginManager->GetLoginStage() == ELoginStage::StageRoleLogin))
		{
			if (IsValid(UUECS3GameInstance::Instance->GUIManager))
			{
				UUECS3GameInstance::Instance->GUIManager->HideVSWindows();
			}
			//如果关卡加载完毕，掉线了，切换回登录关卡
			UGolbalBPFunctionLibrary::LevelManager()->TeleportLoginLevel();
			CS3_Log(TEXT("UGameStatus::CheckChangeStatus: ++++++++++++++%i false; Because is not StageRoleLogin!"), (int)InStatus);
			return false;
		}
	}
	return true;
}


void UGameStatus::ChangeStatus(EGameStatus status)
{
	if (!CheckChangeStatus(status))
	{
		return;
	}
	static UEnum* EnumPtr = FindObject<UEnum>(ANY_PACKAGE, TEXT("EGameStatus"), true);
	CSV_EVENT_GLOBAL(TEXT("GameStatus %s"), *EnumPtr->GetNameByValue((int64)status).ToString());
	CS3_Log(TEXT("UGameStatus::ChangeStatus: ++++++++++++++%i"), (int)status );
	LastStatus = CurrStatus;
	CurrStatus = status;

	if (status == EGameStatus::InWorld)
	{
		OnChangeInWorldStatus();
	}
	else if (status == EGameStatus::Teleport)
	{
		OnChangeTeleportStatus();
	}
	else if (status == EGameStatus::SelectRole)
	{
		OnChangeSelectRoleStatus();
	}
	else if (status == EGameStatus::CreateRole)
	{
		OnChangeSelectCreateRole();
	}
	else if (status == EGameStatus::SelectCamp)
	{
		OnChangeSelectSelectCamp();
	}
	else if (status == EGameStatus::Login)
	{
		OnChangeLogin();
	}
	else if (status == EGameStatus::Personalize)
	{
		OnChangeOverEvent();
	}
	// 游戏状态改变蓝图回调
	OnGameStatusChangeBP();
}

void UGameStatus::OnChangeSelectRoleStatus()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeSelectRoleStatus----------"));
	UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld = true;
	OnChangeOverEvent();
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if (MediaPlayerManager)
	{
		MediaPlayerManager->PreLoadMediaAssetByGameStatus();
	}
}

void UGameStatus::OnChangeSelectCreateRole()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeSelectCreateRole----------"));
	OnChangeOverEvent();
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if (MediaPlayerManager)
	{
		MediaPlayerManager->PreLoadMediaAssetByGameStatus();
	}
}

void UGameStatus::OnChangeSelectSelectCamp()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeSelectSelectCamp----------"));
	OnChangeOverEvent();
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if (MediaPlayerManager)
	{
		MediaPlayerManager->PreLoadMediaAssetByGameStatus();
	}
}


void UGameStatus::OnChangeTeleportStatus()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeTeleportStatus----------"));
	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(true, EGameStatus::InWorld, TEXT("SwitchScene"));
	}

	if (IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		///<清除音频数据
		UGolbalBPFunctionLibrary::AudioManager()->ClearAudioData();
	}

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		///<停止飞行传送
		PlayerCharacter->SwitchOffFlyOrbitMode();
	}

	if (IsValid(UUECS3GameInstance::Instance->GStoryManager) )
	{
		//停止播放镜头并清除镜头缓存
		if (UUECS3GameInstance::Instance->GStoryManager->IsStopLoadingLevel())
		{
			UUECS3GameInstance::Instance->GStoryManager->StopSequence();
			UUECS3GameInstance::Instance->GStoryManager->ClearStoryAsset();
		}
	
	}
	if (IsValid(UUECS3GameInstance::Instance->MediaPlayerManager))
	{
		if (UUECS3GameInstance::Instance->MediaPlayerManager->IsStopLoadingLevel())
		{
			///<清除媒体播放器缓存
			//UUECS3GameInstance::Instance->MediaPlayerManager->Close();
			UUECS3GameInstance::Instance->MediaPlayerManager->ClearMediaAsset();
		}
	}

	// 加载关卡，暂停区域检测；加载完再开始
	UUECS3GameInstance::Instance->MapManager->PauseAreaDetectTimer();

	CS3PlayRole *MyRolePlayer = UUECS3GameInstance::Instance->CS3Player();
	if (MyRolePlayer)
	{
		MyRolePlayer->OnLeaveScenes();
	}

	///清空状态管理器里的数据 播放镜头中不做处理
	ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(CS3PlayerController) &&	IsValid(UUECS3GameInstance::Instance->GStoryManager) && !UUECS3GameInstance::Instance->GStoryManager->IsPlaying() &&
		IsValid(UGolbalBPFunctionLibrary::LevelManager()) && UGolbalBPFunctionLibrary::LevelManager()->GetSubStreamLevelName().IsNone())
	{
		UAtkStateMar* AtkStateMar= CS3PlayerController->GetAtkStateMar();
		if (IsValid(AtkStateMar))
		{
			AtkStateMar->Leave();
		}		
	}
}

void UGameStatus::OnChangeInWorldStatus()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeInWorldStatus----------"));
	//玩家在进入位面中播放背景和环境音效
	if (LastStatus != EGameStatus::Teleport)
	{
		UGolbalBPFunctionLibrary::AudioManager()->PlaySceneAndEnvironmentMusic();
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		///<设置玩家的快捷键
		if (IsValid(PlayerController->GetStateCtrlComp()))
		{
			PlayerController->GetStateCtrlComp()->UpdateStortcutKeyData(true);
			PlayerController->DynamicBindInputEvent(true, true);
		}
		//玩家接收输入输出
		//PlayerController->EnableInputToControll(true);
	}
	if (!IsValid(UUECS3GameInstance::Instance))return;

	//重启区域检测
	if (IsValid( UUECS3GameInstance::Instance->MapManager ))
	{
		UUECS3GameInstance::Instance->MapManager->UnPauseAreaDetectTimer();
	}
	
	//清除幻兽缓存
	if (IsValid(UUECS3GameInstance::Instance->CharacterRideManager))
	{
		UUECS3GameInstance::Instance->CharacterRideManager->ClearCacheData();
	}
	
	if (UGolbalBPFunctionLibrary::LoginManager() && UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld)
	{
		//进入世界时通知GUIManager
		UGUIManager* GUIManager = UUECS3GameInstance::Instance->GUIManager;
		if (GUIManager)
		{
			GUIManager->OnRoleEnterWorld();
		}

		//添加区域检测timer
		UMapManager* MapManager = UUECS3GameInstance::Instance->MapManager;
		if (MapManager)
		{
			MapManager->AddAreaDetectTimer();
		}

		UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld = false;
	}
}

void UGameStatus::OnChangeLogin()
{
	CS3_Display(CS3DebugType::CL_Status, TEXT("GameStatus::OnChangeLogin----------"));
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if (MediaPlayerManager)
	{
		//预加载媒体资源
		MediaPlayerManager->PreLoadMediaAssetByGameStatus();
	}
	UGolbalBPFunctionLibrary::LoginManager()->bIsFirstEnterWorld = true;
	OnChangeOverEvent();
	LoginLoadingOver.Broadcast();
}

void UGameStatus::OnChangeOverEvent()
{
	CS3_Warning(TEXT("GameStatus::GetIsLoginStatus:-----------"));
	//如果关卡加载完毕，掉线了，切换回登录关卡
	if ( IsValid(UGolbalBPFunctionLibrary::LoginManager())&&!UGolbalBPFunctionLibrary::LoginManager()->GetIsLoginStatus() && !IsCurrStatus(EGameStatus::Login))
	{
		UGolbalBPFunctionLibrary::LevelManager()->TeleportLoginLevel();
		return;
	}

	//CST-11823事务限制刚进游戏时的限制输入
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->EnableInputToControll(true);
	}

	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		UBaseWindow* SwitchSceneWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("SwitchScene"));
		if (IsValid(SwitchSceneWindow))
		{
			///<关闭加载界面
			SwitchSceneWindow->Hide();
		}
	}
	///<开启渲染
	GEngine->RedrawViewports(true);
	if (IsValid(UGolbalBPFunctionLibrary::LevelManager()))
	{
		///<处理流关卡下TureSky问题
		//UGolbalBPFunctionLibrary::LevelManager()->ForceCloseTrueSky();
	}
	if (IsValid(UGolbalBPFunctionLibrary::AudioManager()))
	{
		///<播放背景音乐和环境音乐
		UGolbalBPFunctionLibrary::AudioManager()->PlaySceneAndEnvironmentMusic();
	}
}

void UGameStatus::OnInWorldLoadingOver()
{
	OnChangeOverEvent();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		///<摄像机处理
		PlayerCharacter->ResetCameraData();
		PlayerCharacter->OnClearCameraParamsEventTimer();
	}

	if (IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		//显示所有界面
		if (!UGolbalBPFunctionLibrary::GUIManager()->IsShowVSWindows()&& 
			IsValid(UUECS3GameInstance::Instance->GStoryManager)&&
			!UUECS3GameInstance::Instance->GStoryManager->IsPlaying())
		{
			UGolbalBPFunctionLibrary::GUIManager()->HideOrShowVSWindows(false);
		}		 
	}
	
	if (IsValid(UGolbalBPFunctionLibrary::GStoryManager()))
	{
		///<预加载镜头播放
		UGolbalBPFunctionLibrary::GStoryManager()->PreLoadStory(FSTRING_TO_FNAME(UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"))));
		
		///<后台加载镜头
		UGolbalBPFunctionLibrary::GStoryManager()->PreLoadAllStoryAsset();
	}
	///<通知服务器客户端某个地图已经加载完毕
	CS3Role *  pEntity_Player = (CS3Role *)UUECS3GameInstance::pKBEApp->Player();

	if (!pEntity_Player || !pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGameStatus::OnInWorldLoadingOver : pEntity_Player || pEntity_Player->IsPlayerRole()!"));
	}
	else
	{
		(pEntity_Player)->LoadSpaceCompleted();
	}
	///判断当前进地图操作 是否为goto进入位面
	if (!UGolbalBPFunctionLibrary::LevelManager()->GotoIsPlane)
	{
		//进地图提示
		UUECS3GameInstance::Instance->MapManager->SendEnterSpaceMsg();
	}
	//后台加载媒体资源
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if (MediaPlayerManager)
	{
		MediaPlayerManager->PreLoadAllMediaAsset();
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UGameStatus::OnInWorldLoadingOver: InWorld Loading Over!"));
	BP_OnInWorldLoadingOver();
	SetIsInWorldLoadingOver(true);
	InWorldLoadingOver.Broadcast();
}

CONTROL_COMPILE_OPTIMIZE_END
// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleSpaceInterface.h"
#include "Actor/ServerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameData/GameDeFine.h"
#include "GameData/ConstData.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Manager/LevelManager.h"
#include "Manager/MapManager.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/BaseWindow.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "UMG/Public/Blueprint/UserWidget.h"
#include "MoviePlayer/Public/MoviePlayer.h"
#include "Manager/GameStatus.h"
#include "Util/ConvertUtil.h"
#include "Manager/SystemSwitchManager.h"
#include "Interface/Role/RoleSpaceContentInterface.h"

// 开始和结束加载地图回调
static FDelegateHandle BeginLoadDelegateHandle;
static FDelegateHandle EndLoadDelegateHandle;

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleSpaceInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleSpaceInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void URoleSpaceInterface::OnEnterSpaceNotify_Implementation(const FString& SpaceScriptID, const INT32 SpaceType)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Player Enter Space Notify. scriptID:%s, spaceType:%i.------------>>>"), *SpaceScriptID, SpaceType);

	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->GameStatus)
	{
		UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.RemoveDynamic(this, &URoleSpaceInterface::OnEnterSpaceNotifyEntrust);
	}

	if (UUECS3GameInstance::Instance->GameStatus->GetIsInWorldLoadingOver())
	{
		if (SpaceType == int(ENUM_SPACE_TYPE::SPACE_TYPE_PLANE))	//位面 
		{
			OnEnterPlane();
		}

		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (IsValid(PlayerController))
		{
			PlayerController->EnableInputToControll(true);
		}
		
		OnEnterSpaceNotifyBP(SpaceType);
		//系统开启
		if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->SystemSwitchManager)
		{
			UUECS3GameInstance::Instance->SystemSwitchManager->OnEnterSpaceNotify(SpaceScriptID);
		}
	}
	else
	{
		SpaceScriptid = SpaceScriptID;
		Spacetype = SpaceType;
		if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->GameStatus)
		{
			UUECS3GameInstance::Instance->GameStatus->InWorldLoadingOver.AddDynamic(this, &URoleSpaceInterface::OnEnterSpaceNotifyEntrust);
		}
	}
}

void URoleSpaceInterface::OnEnterSpaceNotifyEntrust()
{
	OnEnterSpaceNotify(SpaceScriptid, Spacetype);
}


void URoleSpaceInterface::OnEnterAreaNotify_Implementation()
{
	OnEnterAreaNotifyEvent.Broadcast();
	//转到玩家背后视角
	SetPlayerRotation();
}

void URoleSpaceInterface::OnLoginSpaceNotify_Implementation(const FString& SpaceScriptID, const INT32 SpaceType)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Player Login Space Notify. scriptID:%s, spaceType:%i.------------>>>"), *SpaceScriptID, SpaceType);
	OnLoginSpaceNotifyBP(SpaceType);
}

void URoleSpaceInterface::OnLeaveSpaceNotify_Implementation(const FString& ScriptID, const FString& SpaceType)
{
	//通知UIManager关闭所有打开的界面
	if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->GUIManager)
	{
		UUECS3GameInstance::Instance->GUIManager->OnLeaveSpaceNotify();
	}

	const FString _ScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	const FString _SpaceType = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_TYPE")));

	OnleavePlane();

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Player LeaveSpace Notify. SpaceData:[scriptID:%s, spaceType:%s]. Args:[scriptID:%s, spaceType:%s]"), *_ScriptID, *_SpaceType, *ScriptID, *SpaceType);
	//这里之所以使用传进来的参数，是因为OnLeaveSpaceNotify有可能被缓存了，但是SpaceData的中的数据并没有做如此的处理。
	OnLeaveSpaceNotifyBP(ScriptID, SpaceType);
	if(ScriptID.Equals("fu_ben_L_YCJMD_zhenyingPVP"))
	{
		URoleSpaceContentInterface* SCInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), 0));
		if(IsValid(SCInterface))
		{
			SCInterface->SetIsEnabledQuickBar(true);
		}

	}
}

void URoleSpaceInterface::SeamLessLoadLevel_Implementation()
{
	IsPlaneLoading(true);
}

void URoleSpaceInterface::GotoSpacePlane_Implementation(const FString& ScriptID)
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor))
	{
		const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
		if (SpaceScriptID.Compare(ScriptID))
		{
			Cast<APlayerCharacter>(PlayerActor)->OnTriggerPlane(ScriptID);			
		}
	}
}

void URoleSpaceInterface::LeaveSpacePlane_Implementation(const FString& ScriptID)
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor))
	{
		Cast<APlayerCharacter>(PlayerActor)->OnTriggerPlane(ScriptID, true);
	}
}

void URoleSpaceInterface::OnEnterPlane()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Player Enter Plane------------>>>"));
	Notify_CreateLightWall();
}

void URoleSpaceInterface::OnleavePlane()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->EnableInputToControll(false);
	}
}

void URoleSpaceInterface::RequestGoToSpace()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RequestGoToSpace : GetEntity()!"));
		return;
	}
	FAreaReviveData ReviveData = UUECS3GameInstance::Instance->MapManager->GetAreaReviveData();
	FString SpaceScriptID = ReviveData.ReviveSpace;
	if (SpaceScriptID.IsEmpty())
	{
		SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID"));
	}
	FVector Position = ReviveData.RevivePosition;
	FVector Direction = FVector::ZeroVector;
	Direction.Z = ReviveData.ReviveDirection.Euler().Z;
	KBEngine::FVariantArray args;
	if (Position.IsZero())
	{
		RPC_requestGotoDynamicRevivePos();
		//GetEntity()->CellCall(TEXT("requestGotoDynamicRevivePos"), args);
	}
	else
	{
		RPC_RequestGoToSpace(SpaceScriptID, Position, Direction);
		//args.Add(SpaceScriptID);
		//args.Add(Position);
		//args.Add(Direction);
		//GetEntity()->CellCall(TEXT("requestGoToSpace"), args);
	}
}
void URoleSpaceInterface::RPC_RequestGoToSpace(FString SpaceScriptID, FVector Position, FVector Direction)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_RequestGoToSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(SpaceScriptID);
	args.Add(Position);
	args.Add(Direction);
	entity->CellCall(TEXT("requestGoToSpace"), args);
}

void URoleSpaceInterface::RPC_requestGotoDynamicRevivePos()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_requestGotoDynamicRevivePos : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("requestGotoDynamicRevivePos"), args);
}

void URoleSpaceInterface::ChangeMovementMode(const uint8& MovementMode)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	bool bUseCharacterMovement;
	if (PlayerController)
	{
		if (MovementMode == 0)
		{
			bUseCharacterMovement = false;
		}
		else
		{
			bUseCharacterMovement = true;
		}
		PlayerController->ChangeMoveMode(CHANGE_CHARACTER_MOVEMENT_TYPE::CHANGE_CHARACTER_MOVEMENT_TYPE_SPACE_COPY,bUseCharacterMovement);
	}
}

void URoleSpaceInterface::FlyToSubSpace(FString fPatrolID, FString sPatrolID, int32 sPoint, int32 pPoint, float speed, FVector enterPos)
{
	APlayerCharacter* playerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(playerActor))
	{
		playerActor->EnterFlyToHZMGSpace(fPatrolID, sPatrolID, sPoint, pPoint, speed, enterPos);
	}
}

void URoleSpaceInterface::StopFlyToSubSpace(FString fPatrolID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor) && GetEntity()->IsPlayer())
	{
		PlayerActor->StopFlyToHZMGSpace(fPatrolID);
	}
}

void URoleSpaceInterface::ShowMazeDice_Implementation(bool IsVisible_)
{
	APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
	if (player)
	{
		player->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		player->RideCarrierComponent->RideOnCarrier(CARRIER_ID);

	}
}

void URoleSpaceInterface::ShowMazeNum_Implementation(int MazeNum)
{

}

void URoleSpaceInterface::GetSpaceEntityRecordPos(FString SctriptID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::GetSpaceEntityRecordPos : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SctriptID);
	GetEntity()->CellCall(TEXT("requestEntityRecodPos"), args);
}
void URoleSpaceInterface::OnGetSpaceEntityRecordPos_Implementation(const FString& PosStr)
{
	
}

void URoleSpaceInterface::SetCanWalkOffLedges_Implementation(bool bCanWalkOffLedges)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (PlayerActor)
	{
		PlayerActor->SetWalkOffLedges(bCanWalkOffLedges);
	}
}

void URoleSpaceInterface::RequestGotoExitSpace()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RequestGotoExitSpace : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("requestGotoExitSpace"), args);
}

void URoleSpaceInterface::RPC_requestGotoExitSpace()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_requestGotoExitSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("requestGotoExitSpace"), args);
}

void URoleSpaceInterface::RPC_clickedBtnGotoExitSpace()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_clickedBtnGotoExitSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("clickedBtnGotoExitSpace"), args);
}

void URoleSpaceInterface::RPC_clickedBtnGotoExitSpaceTTT()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_clickedBtnGotoExitSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("clickedBtnGotoExitSpaceByTongTianTa"), args);
}

void URoleSpaceInterface::RPC_DisconnectDeathToSpace()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceContentInterface::RPC_DisconnectDeathToSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("DisconnectDeathToSpace"), args);
}

void URoleSpaceInterface::CELL_RequestGotoLineNumberSpace(uint8 lineNumber)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::CELL_RequestGotoLineNumberSpace : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(lineNumber);
	entity->CellCall(TEXT("requestGotoLineNumberSpace"), args);
}

void URoleSpaceInterface::CLIENT_RequestGotoLineNumberSpaceFailure_Implementation()
{

}

void URoleSpaceInterface::OnSetSpaceData(uint32 spaceID, const FString& key, const FString& value)
{
	if (key == "SPACE_SCRIPT_ID")
	{
		UUECS3GameInstance::Instance->LevelManager->OnSetSpaceData(spaceID, key, value);
	}
	else if (key == "SPACE_RELATION_MODE")
	{
		UUECS3GameInstance::Instance->SpaceEntityRelationMgr->InitEntityRelationIns(value);
	}
	else if (key == "SPACE_DATA_MAX_LINE_NUMBER")
	{
		OnSpaceMaxLineNumberChanged();
	}
	else if (key == "SPACE_DATA_LINE_NUMBER")
	{
		OnSetSpaceLineNumber();
	}
}

void URoleSpaceInterface::SetPlayerRotation()
{
	///转到玩家背后视角
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor) && IsValid(PlayerActor->GetController()))
	{
		FRotator Rotation = PlayerActor->GetActorRotation();
		PlayerActor->GetController()->SetControlRotation(Rotation - FRotator(17.0f, 0.0f, 0.0f));
	}
}

void URoleSpaceInterface::Notify_CreateLightWall()
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::Notify_CreateLightWall : GetActor()!"));
		return;
	}
	TArray<FVector2D> Polygon = UUECS3GameInstance::Instance->MapManager->GetPlanePolygon();

	if (Polygon.Num() < 2)
	{
		return;
	}
	const FString Level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	Cast<APlayerCharacter>(GetActor())->CreateLightWall(Level, AREA_LIGHT_WALL_TYPE_ENUM::AreaLightWall);
}

void URoleSpaceInterface::CLIENT_ArticleToReadNotify_Implementation(const int32 spaceID)
{
	FString spaceIDValue = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	UUECS3GameInstance::Instance->LevelManager->OnSetSpaceData(spaceID, TEXT("SPACE_SCRIPT_ID"), spaceIDValue, LOADING_MODE_ENUM::LOADING_MODE_FORCE);
}

void URoleSpaceInterface::CLIENT_StartVideoLoading_Implementation()
{

	TWeakObjectPtr <URoleSpaceInterface> ThisPtr(this);
	// 隐藏界面，这个不能放在地图加载回调中
	OnVideoLoadingStartPlay();
	BeginLoadDelegateHandle = FCoreUObjectDelegates::PreLoadMap.AddLambda([ThisPtr](const FString& LevelName)
	{
		FLoadingScreenAttributes LoadingScreen;

		LoadingScreen.bAutoCompleteWhenLoadingCompletes = false;
		LoadingScreen.bMoviesAreSkippable = false;
		LoadingScreen.bWaitForManualStop = true;
		LoadingScreen.PlaybackType = EMoviePlaybackType::MT_Looped;

		LoadingScreen.WidgetLoadingScreen = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("SwitchScene"))->TakeWidget();
		LoadingScreen.MoviePaths.Add("xunhuan");

		// 播放视频
		GetMoviePlayer()->SetupLoadingScreen(LoadingScreen);
	});
	EndLoadDelegateHandle = FCoreUObjectDelegates::PostLoadMapWithWorld.AddLambda([ThisPtr](UWorld* World)
	{
		// 结束播放
		GetMoviePlayer()->StopMovie();

		// 显示背景图片和进度条
		if (ThisPtr.IsValid())
		{
			ThisPtr.Get()->OnVideoLoadingEndPlay();
		}
		
		// 播放解除绑定
		FCoreUObjectDelegates::PostLoadMapWithWorld.Remove(EndLoadDelegateHandle);
		FCoreUObjectDelegates::PreLoadMap.Remove(BeginLoadDelegateHandle);
	
	});
}

void URoleSpaceInterface::OnVideoLoading_Implementation(const FString& NextLevel, const int32& IsLoadBG, const int32& IsLoadDoor)
{
	VideoLoadData.NextLevel = NextLevel;
	VideoLoadData.IsLoadBG = IsLoadBG;
	VideoLoadData.IsLoadDoor = IsLoadDoor;
}

void URoleSpaceInterface::OnNotifyPreloadSpace_Implementation(const FString& preloadLevel, const int32& isPreload)
{
	VideoLoadData.NextLevel = preloadLevel;
	VideoLoadData.IsLoadBG = isPreload;
}

void URoleSpaceInterface::AgainNotifySpaceData_Implementation(const FString& InSpaceScriptID)
{
	if (UGolbalBPFunctionLibrary::LevelManager())
	{
		UGolbalBPFunctionLibrary::LevelManager()->AgainTeleportSubStreamLevel(FSTRING_TO_FNAME(InSpaceScriptID));
	}
}

void URoleSpaceInterface::OnRep_disableAssistJump()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::OnRep_disableAssistJump() : GetEntity()!"));
		return;
	}
	if (GetEntity()->IsPlayer())
	{
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(PlayerActor))
		{
			//1为关闭辅助跳，0为不关闭
			int32 disableAssistJump = GetEntity()->GetDefinedProperty(TEXT("disableAssistJump"));
			PlayerActor->IsLevelOpenLedgesJump = disableAssistJump == 0 ? true : false;
		}
	}
}

void URoleSpaceInterface::InitBlueCB()
{
	ArrBlueFunc.Add("SeamLessLoadLevel");
	ArrBlueFunc.Add("OnEnterSpaceNotify");
	ArrBlueFunc.Add("OnLoginSpaceNotify");
	ArrBlueFunc.Add("OnLeaveSpaceNotify");
	ArrBlueFunc.Add("GotoSpacePlane");
	ArrBlueFunc.Add("LeaveSpacePlane");
	ArrBlueFunc.Add("ChangeMovementMode");
	ArrBlueFunc.Add("FlyToSubSpace");
	ArrBlueFunc.Add("StopFlyToSubSpace");
	ArrBlueFunc.Add("ShowMazeDice");
	ArrBlueFunc.Add("ShowMazeNum");
	ArrBlueFunc.Add("GetSpaceEntityRecordPos");
	ArrBlueFunc.Add("OnGetSpaceEntityRecordPos");
	ArrBlueFunc.Add("OnEnterAreaNotify");
	ArrBlueFunc.Add("SetCanWalkOffLedges");
	ArrBlueFunc.Add("CLIENT_RequestGotoLineNumberSpaceFailure");
	ArrBlueFunc.Add("CLIENT_ArticleToReadNotify");
	ArrBlueFunc.Add("CLIENT_StartVideoLoading");
	ArrBlueFunc.Add("OnVideoLoading");
	ArrBlueFunc.Add("AgainNotifySpaceData");
	ArrBlueFunc.Add("OnNotifyPreloadSpace");
	Supper::InitBlueCB();
}


CONTROL_COMPILE_OPTIMIZE_END
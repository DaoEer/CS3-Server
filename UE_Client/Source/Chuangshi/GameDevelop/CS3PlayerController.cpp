// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3PlayerController.h"
#include "CS3Base/CS3EntityInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Actor/ServerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleStateInterface.h"
#include "Runtime/JsonUtilities/Public/JsonObjectConverter.h"
#include "Chuangshi/Actor/Player/PlayerCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Runtime/Engine/Classes/Engine/UserInterfaceSettings.h"
#include "GameData/ModelPartData.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Manager/ResourceManager.h"
#include "Manager/QTEManager.h"
#include "GameFramework/InputSettings.h"
#include "Manager/MessageManager.h"
#include "Component/Role/JumpComponent.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/MapManager.h"
#include "Manager/GameStatus.h"
#include "CS3Base/UIFixerManager.h"
#include "Manager/TutorialManager.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/AtkStateMar.h"
#include "CS3ConsoleMgr.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "Manager/CustomTimerManager.h"
#include "Interface/Role/RolePetInterface.h"
#include "Actor/NPC/NPCCharacter.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/RoleActivityInterface.h"
#include "Manager/VisibleManager.h"
#include "Kismet/KismetSystemLibrary.h"
#include "GameData/GameDefault.h"
#include "CS3GameInstance.h"
#include "GameData/ConstDataBP.h"



CONTROL_COMPILE_OPTIMIZE_START

ACS3PlayerController::ACS3PlayerController()
{
	// 设置鼠标事件
	bShowMouseCursor = true;
	bEnableClickEvents = true;
	bEnableMouseOverEvents = true;
	//bEnableTouchOverEvents = true;
	// 添加鼠标事件
	ClickEventKeys.AddUnique(EKeys::RightMouseButton);

	// 角色控制状态组件
	RoleCtrlStateMgr = CreateDefaultSubobject<URoleCtrlStateMgr>(TEXT("RoleCtrlStateMgr"));
	RoleCtrlStateMgr->OnEnterState(EROLE_CTRL_STATE::RCS_COMMON);

	CS3ConSoleMgr = CreateDefaultSubobject<UCS3ConsoleMgr>(TEXT("CS3ConSoleMgr"));
	
	// 角色移动控制组件
	MoveControlComponent = CreateDefaultSubobject<UPlayerControllerMoveComponent>(TEXT("MoveControlComponent"));

	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CS3PC = this;
	}

	//增加那些按键不在切换焦点时刷新
	FlushKeyStateMapSkip = { {EKeys::W, FKeyState()}, {EKeys::A, FKeyState()}, {EKeys::S, FKeyState()}, {EKeys::D, FKeyState()} };
}

void ACS3PlayerController::BeginPlay()
{
	Super::BeginPlay();

	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}

	const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	//用户系统设置
	if (GameInstance &&
		GameInstance->LocalDataSaveManager &&
		GameInstance->LocalDataSaveManager->LocalUserSettingData
		)
	{
		ULocalUserSettingData* LocalUserSettingData = GameInstance->LocalDataSaveManager->LocalUserSettingData;
		
		//用户系统设置文件是否存在，若不存在，则初始化数据
		if (!GameInstance->LocalDataSaveManager->DeosLocalUserSettingDataExist())
		{
			LocalUserSettingData->InitLocalUserSettingData();
			GameInstance->LocalDataSaveManager->SaveLocalUserSettingDataFile();
		}
		if (!LocalUserSettingData->bApplyResolutionChanged)
		{
			LocalUserSettingData->ApplySystemSettingData();
			LocalUserSettingData->bApplyResolutionChanged = true;
		}
	}

	NewReso = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
	if (NewReso.IsZero())
	{
		CS3_Warning(TEXT("-->error:ACS3PlayerController::BeginPlay : ViewportSize IsZero !"));
	};
	PreReso = NewReso;
	PreScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(PreReso.X, PreReso.Y));
	GEngine->GameViewport->Viewport->ViewportResizedEvent.AddUObject(this, &ACS3PlayerController::OnResolutionChanged);
	UUECS3GameInstance::Instance->CS3PC = this;

	AtkStateMar = NewObject<UAtkStateMar>();

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	UCustomCursorManager* CustomCursorManager = UGolbalBPFunctionLibrary::CustomCursorManager();

	//控制模式初始化
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->Init();
	}
	//操作模式初始化
	if (IsValid(OperationModeMgr))
	{
		OperationModeMgr->Init();
	}
	//鼠标数据初始化
	if (IsValid(CustomCursorManager))
	{
		CustomCursorManager->Init();
	}

	//设置默认的摄像机旋转速度
	fDefaultCameraRotateScale = InputYawScale;
	///<设置禁止输入
	EnableInputToControll(false);
}

void ACS3PlayerController::SetMousePosition(float LocationX, float LocationY)
{
	FViewport* Viewport = CastChecked<ULocalPlayer>(this->Player)->ViewportClient->Viewport;
	int IntX = (int)LocationX;
	int IntY = (int)LocationY;
	Viewport->SetMouse(IntX, IntY);
}

void ACS3PlayerController::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);

	if (IsLocalController())
	{
		ConsumeKeyMovementInput();
	}
}

void ACS3PlayerController::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CS3PC = nullptr;
	}
	Super::EndPlay(EndPlayReason);
}

void ACS3PlayerController::GetSeamlessTravelActorList(bool bToEntry, TArray<class AActor*>& ActorList)
{
	
	if (MoveActors.Num()>0)
	{
		ActorList.Append(MoveActors);
	}
	else
	{
		CS3_Warning(TEXT("Try to Teleport inValid Player!"));
	}
	Super::GetSeamlessTravelActorList(bToEntry, ActorList);
}



void ACS3PlayerController::OnMouseLeftButtonClick()
{
	if (!CheckBindActionActive(FName("MouseLeftClick"))) return;
	
	//调用控制模式管理器
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (!IsValid(ControllerModeMgr))
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnMouseLeftButtonClick --- ControllerModeMgr Is Null!"))
		return;
	}

	TArray<FString> OtherValue;

	ControllerModeMgr->ExecuteInputInfor(TEXT("MouseLeftClick"), TEXT(""), 0.0f, OtherValue);
}

void ACS3PlayerController::OnMouseRightButtonClick()
{
	if (!CheckBindActionActive(FName("MouseRightClick"))) return;

	//调用控制模式管理器
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (!IsValid(ControllerModeMgr))
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnMouseRightButtonClick --- ControllerModeMgr Is Null!"))
			return;
	}

	TArray<FString> OtherValue;

	ControllerModeMgr->ExecuteInputInfor(TEXT("MouseRightClick"), TEXT(""), 0.0f, OtherValue);
}

void ACS3PlayerController::OnJumpPressed()
{
	if (!CheckBindActionActive(FName("Jump"))) return;
	/*	APlayerCharacter* MyCharacter = Cast<APlayerCharacter>(UUECS3GameInstance::Instance->GetPlayerActor());
	   if (MyCharacter && IsCanJump())
	   {
		   MyCharacter->OnCheckJumpSkill();
	   }*/

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		ControllerModeMgr->ChangeControlModeFromACTToALT(false);
		TArray<FString> OtherValue;

		ControllerModeMgr->ExecuteInputInfor(TEXT("JumpPressed"),TEXT(""),0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnJumpReleased()
{
	if (!CheckBindActionActive(FName("Jump"))) return;
	/*AServerCharacter* MyCharacter = Cast<AServerCharacter>(UUECS3GameInstance::Instance->GetPlayerActor());
	if (IsValid(MyCharacter))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("JumpJump StopJumping[Start====JumpCurrentCount=%d,  bPressedJump=%d, bWasJumping=%d]"), MyCharacter->JumpCurrentCount, MyCharacter->bPressedJump, MyCharacter->bWasJumping);
		if (MyCharacter->bPressedJump)
		{
			FTimerHandle DelayHandle;
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle,this,&ACS3PlayerController::OnStopJumping, 0.1f, false);
			}
		}
		else
		{
			MyCharacter->StopJumping();
		}
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("JumpJump StopJumping[end====JumpCurrentCount=%d,  bPressedJump=%d, bWasJumping=%d]"), MyCharacter->JumpCurrentCount, MyCharacter->bPressedJump, MyCharacter->bWasJumping);
	}*/

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("JumpReleased"), TEXT(""), 0.0f, OtherValue);
	}
} 

void ACS3PlayerController::OnShowSystemUI()
{
	if (!CheckBindActionActive(FName("SystemUI"))) return;

	//调用控制模式管理器
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (!IsValid(ControllerModeMgr))
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnShowSystemUI --- ControllerModeMgr Is Null!"))
			return;
	}

	TArray<FString> OtherValue;

	ControllerModeMgr->ExecuteInputInfor(TEXT("EscClick"), TEXT(""), 0.0f, OtherValue);
}

bool ACS3PlayerController::ProcessConsoleExec(const TCHAR* Cmd, FOutputDevice& Ar, UObject* Executor)
{

	bool ret = Super::ProcessConsoleExec(Cmd, Ar, Executor);
	if (!ret&&CS3ConSoleMgr)
	{
		ret = CS3ConSoleMgr->ProcessConsoleExec(Cmd, Ar, Executor);
	}
	return ret;
}
bool ACS3PlayerController::CanMoveControl(bool isForceMove /*= false*/)
{
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		return false;
	}
	if (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld)
	{
		return false;
	}
	URoleStateInterface* RoleStateInst = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr);
	if (RoleStateInst && RoleStateInst->IsActionForbid(ACTION_FLAG::ACTION_FORBID_MOVE) && !isForceMove)
	{
		CS3_Log(TEXT("ACS3PlayerController::CanMoveControl : RoleStateInst && RoleStateInst->IsActionForbid(ACTION_FLAG::ACTION_FORBID_MOVE)  return false!"));
		return false;
	}
	return true;
}

void ACS3PlayerController::BP_TraceTargetActor(const AActor* TargetActor, const float NearbyRange, FTraceMoveCallback TraceMoveCallback)
{
	TraceTargetActor(TargetActor, NearbyRange, FTraceCallback::CreateLambda([TraceMoveCallback](bool IsSuccess)
	{
		TraceMoveCallback.ExecuteIfBound(IsSuccess);
	}));
}

void ACS3PlayerController::TraceTargetActor(const AActor* TargetActor, const float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	if (!IsFlying() && CanMoveControl())
	{
		MoveControlComponent->TraceTargetActor(TargetActor, NearbyRange, TraceCallback, IsStopMove, TraceStopMoveCallback);
	}
	else
	{
		TraceCallback.ExecuteIfBound(false);
	}
}

void ACS3PlayerController::TraceTargetActorAtClient(const AActor* TargetActor, const float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	if (!IsFlying() && CanMoveControl())
	{
		MoveControlComponent->TraceTargetActorAtClient(TargetActor, NearbyRange, TraceCallback, IsStopMove, TraceStopMoveCallback);
	}
	else
	{
		TraceCallback.ExecuteIfBound(false);
	}
}

void ACS3PlayerController::TeamFollowTraceTarget(const AActor* TargetActor, const float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	if (!IsFlying() && CanMoveControl(true))
	{
		MoveControlComponent->TeamFollowTraceTarget(TargetActor, NearbyRange, TraceCallback, IsStopMove, TraceStopMoveCallback);
	}
	else
	{
		TraceCallback.ExecuteIfBound(false);
	}
}

void ACS3PlayerController::BP_TraceTargetPostion(const FVector& TargetPostion, const float NearbyRange, FTraceMoveCallback TraceMoveCallback)
{
	TraceTargetPostion(TargetPostion, NearbyRange, FTraceCallback::CreateLambda([TraceMoveCallback](bool IsSuccess)
	{
		TraceMoveCallback.ExecuteIfBound(IsSuccess);
	}));
}

void ACS3PlayerController::TraceTargetPostion(const FVector& TargetPostion, const float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	if (!IsFlying() && CanMoveControl())
	{
		MoveControlComponent->TraceTargetPostion(TargetPostion, NearbyRange, TraceCallback, IsStopMove, TraceStopMoveCallback);
	}
	else
	{
		TraceCallback.ExecuteIfBound(false);
	}
}

void ACS3PlayerController::MoveBackToPostion(const float MoveSpeed, const FVector& TargetPostion)
{
	if (!IsFlying() && CanMoveControl(true))
	{
		MoveControlComponent->MoveBackToPostion(MoveSpeed, TargetPostion);
	}
}

void ACS3PlayerController::EndMoveBack()
{
	MoveControlComponent->EndMoveBack();
}

void ACS3PlayerController::BP_FlyToLocation(const FVector& Location, const bool IsFlyPatrol, const bool bIsFixedDirection, FTraceMoveCallback FlyMoveCallback)
{
	FlyToLocation(Location, IsFlyPatrol, bIsFixedDirection, FTraceCallback::CreateLambda([FlyMoveCallback](bool IsSuccess)
	{
		FlyMoveCallback.ExecuteIfBound(IsSuccess);
	}));
}

void ACS3PlayerController::FlyToLocation(const FVector& Location, const bool IsFlyPatrol /*= false*/, const bool bIsFixedDirection /*= false*/, FTraceCallback FlyCallback /*= FTraceCallback()*/)
{
	MoveControlComponent->FlyToLocation(Location, IsFlyPatrol, bIsFixedDirection, FlyCallback);
}

void ACS3PlayerController::AutoNavigateToLocation(const FVector& DstPosition, FString DstSpaceName /* = "" */, float NearbyRange /* = 2.0f */, FTraceCallback AutoNavigateCallback /* = FTraceCallback() */)
{
	MoveControlComponent->AutoNavigateTargetPosition(DstPosition, DstSpaceName, NearbyRange, AutoNavigateCallback);
}

void ACS3PlayerController::OnTestSpaceAllQuestNavigate(const FString& DstSpaceName, const FString& NPCScriptID)
{
	if (NPCScriptID != "" && SpaceNavigateInfo.Num() > 0)
	{
		SpaceNavigateInfo.Remove(NPCScriptID);
		APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(PlayerActor) && SpaceNavigateInfo.Num() > 0)
		{
			PlayerActor->StartQuestNavigate(true, "", SpaceNavigateInfo[0], DstSpaceName, FVector::ZeroVector, 1.0, 20101000);
		}
	}
}

void ACS3PlayerController::StartJumpInAutoNavigate()
{
	if (!CheckBindActionActive(FName("Jump"))) return;
	APlayerCharacter* MyCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(MyCharacter) && IsValid(MyCharacter->JumpComponent))
	{
		MyCharacter->JumpComponent->OnStartActiveJump();
	}
}

void ACS3PlayerController::ConsumeKeyMovementInput()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor) && !FMath::IsNearlyZero(SuckMoveSpeed))
	{
		FRotator SuckRotator = UGolbalBPFunctionLibrary::GetLookAtRotator(PlayerActor->GetActorLocation(), SuckPosition);
		FVector SuckVector = UKismetMathLibrary::GetForwardVector(SuckRotator);
		float AxisValue = SuckMoveSpeed*100.0f / PlayerActor->GetCharacterMovement()->MaxWalkSpeed;
		MovementInputs.Add(SuckVector*AxisValue);
	}
	if (CanMoveControl())
	{
		MoveControlComponent->ConsumeKeyMovementInput(MovementInputs);
	}
	else
	{
		MovementInputs.Empty();
	}
}	

void ACS3PlayerController::ChangeMoveMode(CHANGE_CHARACTER_MOVEMENT_TYPE ChangeMovementType, bool bIsUseCharacterMovement)
{
	if (bIsUseCharacterMovement)
	{
		ChangeMovementTypes.Add(ChangeMovementType);
	}
	else
	{
		ChangeMovementTypes.Remove(ChangeMovementType);
	}
}

bool ACS3PlayerController::IsCharacterMovementMode()
{
	return true;
	/*if (ChangeMovementTypes.Contains(CHANGE_CHARACTER_MOVEMENT_TYPE::CHANGE_CHARACTER_MOVEMENT_TYPE_SPACE_COPY))
	{
		return true;
	}
	else if (ChangeMovementTypes.Contains(CHANGE_CHARACTER_MOVEMENT_TYPE::CHANGE_CHARACTER_MOVEMENT_TYPE_JUMP))
	{
		return true;
	}
	else
	{
		return false;
	}*/
}

CS3_MOVE_TYPE ACS3PlayerController::GetMoveType()
{
	return MoveControlComponent->GetMoveType();
}

void ACS3PlayerController::StopMove()
{
	MoveControlComponent->StopMove();
}

FFLY_MOVE_INFO ACS3PlayerController::GetFlyMoveInfo()
{
	return MoveControlComponent->GetFlyMoveInfo();
}

bool ACS3PlayerController::IsFlying()
{
	AServerCharacter* Actor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Actor))
	{
		return Actor->GetCharacterMovement()->IsFlying();
	}
	return false;
}


void ACS3PlayerController::SetStateCtrlComp(EROLE_CTRL_STATE CtrlState, bool IsEnter, int32 index/* = 0*/)
{
	//CS3_Warning(TEXT(" ACS3PlayerController::SetStateCtrlComp "));
	if (IsValid(RoleCtrlStateMgr))
	{
		if (IsEnter)
		{
			RoleCtrlStateMgr->OnEnterState(CtrlState, index);
		}
		else
		{
			//CS3_Warning(TEXT(" ACS3PlayerController::SetStateCtrlComp RoleCtrlStateMgr->OnLeaveState"));
			RoleCtrlStateMgr->OnLeaveState(CtrlState);
		}
	}
}

void ACS3PlayerController::SetPlayerControllerMoveComponentTickEnabled(bool bEnabled)
{
	if (IsValid(MoveControlComponent))
	{
		if (bEnabled)
		{
			MoveControlComponent->Activate();
		}
		else
		{
			MoveControlComponent->Deactivate();
		}
	}
}

void ACS3PlayerController::SetupInputComponent()
{
	Super::SetupInputComponent();

	EGameStatus CurStatus = UUECS3GameInstance::Instance->GameStatus->GetCurrStatus();
	EGameStatus LastStatus = UUECS3GameInstance::Instance->GameStatus->GetLastStatus();

	if (CurStatus == EGameStatus::InWorld && LastStatus == EGameStatus::Teleport)
	{
		// 动态配置输入事件
		DynamicBindInputEvent();
	}
}

void ACS3PlayerController::DynamicBindInputEvent(bool bClearOldBind /*= true*/, bool bIsPlayer /*= false*/)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(RoleCtrlStateMgr))
	{
		// 清除已有绑定事件
		if (bClearOldBind)
		{
			TArray<FSHORTCUTKEY>AllKey=	RoleCtrlStateMgr->GetAllShortcutKeyData();
			for (auto& data : AllKey)
			{
				RemoveBindInputData(data.ActName, data.MainKey);
			}
			if (bIsPlayer)
			{
				RoleCtrlStateMgr->InitShortcutKeyDataBySaveData();
			}
		}
		const UInputSettings* InputSettings = GetDefault<UInputSettings>();
		//清除ActionMappings
		TArray<struct FInputActionKeyMapping> ActionMappings = ((UInputSettings*)InputSettings)->ActionMappings;
		for (auto & action : ActionMappings)
		{
			((UInputSettings*)InputSettings)->RemoveActionMapping(action);
		}

		//清除AxisMappings
		TArray<struct FInputAxisKeyMapping> AxisMappings = ((UInputSettings*)InputSettings)->AxisMappings;
		for (auto & axis : AxisMappings)
		{
			((UInputSettings*)InputSettings)->RemoveAxisMapping(axis);
		}

		const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
		bool bIsRecommendMode = true;
		//用户系统设置
		if (GameInstance->LocalDataSaveManager &&
			GameInstance->LocalDataSaveManager->LocalUserSettingData &&
			!GameInstance->LocalDataSaveManager->LocalUserSettingData->CombatSettingData.IsRecommendMode
			)
		{
				bIsRecommendMode = false;
		}
		TArray<FSHORTCUTKEY>AllShortcutKeyData = RoleCtrlStateMgr->GetAllShortcutKeyData();
		for (auto& ShortcutKeyData : AllShortcutKeyData)
		{
			if (!bIsRecommendMode && ShortcutKeyData.KeyType == SHORTCUTKEY_TYPE_ENUM::NORMALMAINQUICKBAR)
			{
				continue;
			}
			else if (bIsRecommendMode && ShortcutKeyData.KeyType == SHORTCUTKEY_TYPE_ENUM::ACTMAINQUICKBAR)
			{
				continue;
			}
			if (ShortcutKeyData.MainKey.Num()>0)
			{
				BindInputData(ShortcutKeyData.ActName, ShortcutKeyData.MainKey);
			}
		}
		BP_DynamicBindInputEvent(bClearOldBind, bIsPlayer);
	}
}

void ACS3PlayerController::SaveShortcutKeyDataToFile(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> NewKeys, TArray<FSHORTCUTKEY>& OldKeys)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		RoleCtrlStateMgr->SaveShortcutKeyDataByTypeToFile(Type, NewKeys, OldKeys);
	}
}

void ACS3PlayerController::ApplyShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type, TArray<FSHORTCUTKEY> OldKeys)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		const UInputSettings* InputSettings = GetDefault<UInputSettings>();
		for (auto& OldKey : OldKeys)
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ApplyShortcutKeyData-->RemoveBindInputData OldKey.ActName=%s"), *FNAME_TO_FSTRING(OldKey.ActName));
			RemoveBindInputData(OldKey.ActName, OldKey.MainKey);
		}

		TArray<FSHORTCUTKEY>ShortcutKeyDatas = RoleCtrlStateMgr->GetShortcutKeyDataByType(Type);
		for (auto& ShortcutKeyData : ShortcutKeyDatas)
		{		
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ApplyShortcutKeyData-->BindInputData ShortcutKeyData.ActName=%s"), *FNAME_TO_FSTRING(ShortcutKeyData.ActName));
			BindInputData(ShortcutKeyData.ActName, ShortcutKeyData.MainKey);
		}
	}	
}

void ACS3PlayerController::CancelShortcutKeyData(SHORTCUTKEY_TYPE_ENUM Type)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		RoleCtrlStateMgr->CancelShortcutKeyData(Type);
	}
}

bool ACS3PlayerController::ChangedShortcutKeysIsEmpty()
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return	RoleCtrlStateMgr->ChangedShortcutKeysIsEmpty();
	}
	return true;
}

TArray<FSHORTCUTKEY> ACS3PlayerController::GetDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return	RoleCtrlStateMgr->GetDefaultShortcutKeyDataByType(Type);
	}
	else
	{
		return{};
	}
}

TArray<FSHORTCUTKEY> ACS3PlayerController::GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return	RoleCtrlStateMgr->GetShortcutKeyDataByType(Type);
	}
	else
	{
		return{};
	}
}

void ACS3PlayerController::RestoreDefaultShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY>OldKeys = GetShortcutKeyDataByType(Type);
	TArray<FSHORTCUTKEY>NewKeys = GetDefaultShortcutKeyDataByType(Type);
	SaveShortcutKeyDataToFile(Type, NewKeys, OldKeys);
	ApplyShortcutKeyData(Type, OldKeys);
}

void ACS3PlayerController::ClearShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM Type)
{
	TArray<FSHORTCUTKEY>ShortcutKeyDatas = GetShortcutKeyDataByType(Type);
	TArray<FSHORTCUTKEY>TempShortcutKeyDatas;
	for (auto &data: ShortcutKeyDatas)
	{
		if (data.CanChange)
		{
			RemoveBindInputData(data.ActName,data.MainKey);
		}
		else
		{
			TempShortcutKeyDatas.Add(data);
		}
	}
	SaveShortcutKeyDataToFile(Type, TempShortcutKeyDatas, ShortcutKeyDatas);
}

FSHORTCUTKEY ACS3PlayerController::ChangeShortcutKeyData(FSHORTCUTKEY ShortcutKey, TArray<FKey>Keys, bool bIsMainKey, FKey OldKey, bool bIsAdd, bool& bIsSuccess, FString& MessageID, FString& Param)
{
	if (!ShortcutKey.CanChange || !(IsValid(RoleCtrlStateMgr)) || Keys.Num() < 1 || (Keys.Num() > 0 && (!Keys[0].IsValid())))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2602);
		bIsSuccess = false;
		return ShortcutKey;
	}
	FGROUPKEY_DATA GroupKey = UGolbalBPFunctionLibrary::ConvertKeysToGroupKey(Keys);
	//键是Alt、Cmd、Ctrl、Shift返回失败
	if ((Keys.Num() == 1 || (!GroupKey.Key.IsValid())) && (GroupKey.Alt || GroupKey.Cmd || GroupKey.Ctrl || GroupKey.Shift))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2601);
		bIsSuccess = false;
		return ShortcutKey;
	}

	//是否双击
	int32 Index = Keys.Find(GroupKey.Key);
	int32 LastIndex = Keys.FindLast(GroupKey.Key);
	if (Index != LastIndex)
	{
		GroupKey.DoubleClick = true;
		if (!ShortcutKey.CanDoubleClick)
		{
			//该功能不能设置键为双击
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2604);
			bIsSuccess = false;
			return ShortcutKey;
		}
	}

	if (!RoleCtrlStateMgr->CheckKeyCanChangeGroupKey(ShortcutKey, GroupKey))
	{
		//该功能不能设置键为某些键
		MessageID = TEXT("4416");
		bIsSuccess = false;
		Param = ShortcutKey.Remarks + TEXT("|") + GroupKey.Key.ToString();
		return ShortcutKey;
	}

	if (!ShortcutKey.CanGroup && (GroupKey.Alt || GroupKey.Cmd|| GroupKey.Ctrl|| GroupKey.Shift))
	{
		//该功能不能设置键为组合键
		MessageID = TEXT("2605");
		bIsSuccess = false;
		return ShortcutKey;
	}

	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ChangeShortcutKeyData-->ShortcutKeyActName =%s"), *FNAME_TO_FSTRING(ShortcutKey.ActName));
	FSHORTCUTKEY OldShortcutKey;
	FSHORTCUTKEY OldChangedShortcutKey;
	
	ESHORTCUT_EXISTING_TYPE result = RoleCtrlStateMgr->CheckShortcutKeyExisting(GroupKey, ShortcutKey.ActName, OldShortcutKey);
	ESHORTCUT_EXISTING_TYPE ChangedResult = RoleCtrlStateMgr->CheckShortcutKeyExistingInChanged(GroupKey, ShortcutKey.ActName, OldChangedShortcutKey);

	switch (result)
	{
	case ESHORTCUT_EXISTING_TYPE::SET_FALSE:
		break;
	case ESHORTCUT_EXISTING_TYPE::SET_TRUE_IN_OLDKEYS:
	{
		///<改变快捷键数据时如果找到本地已保存快捷键，弹出消息框,确定：修改临时快捷键数据对应ActName的快键键为Keys的数据为NONE
		if (RoleCtrlStateMgr->CheckChangedShortcutDataReseted(OldShortcutKey, Keys))
		{
			break;
		}

		if (OldShortcutKey.CanChange)
		{
			MessageID = TEXT("2607");
			Param = FNAME_TO_FSTRING(OldShortcutKey.ActName)+"|"+INT_TO_FSTRING((int32)OldShortcutKey.KeyType);
		}
		else
		{			
			MessageID = TEXT("2608");
			Param = OldShortcutKey.Remarks;
		}

		bIsSuccess = false;
		return ShortcutKey;
	}
	case ESHORTCUT_EXISTING_TYPE::SET_OLDKEYS:
	{
		if (ChangedResult == ESHORTCUT_EXISTING_TYPE::SET_TRUE_IN_CHANGEDKEYS)break;

		///<存在在本地快捷键数据与传过来的数据一样，删除临时修改的快捷键数据返回修改成功
		FSHORTCUTKEY temp;
		RoleCtrlStateMgr->GetShortcutDataByActName(ShortcutKey.KeyType, ShortcutKey.ActName, temp);
		if (temp.Compara(ShortcutKey))
		{
			bIsSuccess = false;
			return ShortcutKey;
		}
		else
		{
			RoleCtrlStateMgr->RemoveShortcutDataFromChangedKeys(ShortcutKey);
			bIsSuccess = true;
			return temp;
		}
	}
	default:
		break;
	}

	switch (ChangedResult)
	{
	case ESHORTCUT_EXISTING_TYPE::SET_FALSE:
		break;
	case ESHORTCUT_EXISTING_TYPE::SET_TRUE_IN_CHANGEDKEYS:
	{	
		if (OldChangedShortcutKey.CanChange)
		{
			MessageID = TEXT("2607");
			Param = FNAME_TO_FSTRING(OldChangedShortcutKey.ActName);
		}
		bIsSuccess = false;
		return ShortcutKey;
	}
	case ESHORTCUT_EXISTING_TYPE::SET_CHANGEDKEYS:
	{
		bIsSuccess = false;
		return ShortcutKey;
	}
	default:
		break;
	}
	///<根据ActName获取默认数据绑定---------------------------
	FInputKeyEvent DefaultMainKey;///<默认数据

	TArray<FSHORTCUTKEY>tempShortcutKeys = RoleCtrlStateMgr->GetDefaultShortcutKeyDataByType(ShortcutKey.KeyType);
	for (auto & data : tempShortcutKeys)
	{
		if (data.ActName == ShortcutKey.ActName)
		{
			if (data.MainKey.Num() < 1)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(2603);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("ChangeShortcutKeyData--->DefaultShortcutKeyData is not Eixting"));
				bIsSuccess = false;
				return ShortcutKey;
			}
			DefaultMainKey = data.MainKey[0];
			break;
		}
	}
	if (DefaultMainKey.KeyDatas.Num() < 1)
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2603);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("ChangeShortcutKeyData--->DefaultShortcutKeyData ActName is not Eixting"));
		bIsSuccess = false;
		return ShortcutKey;
	}

	///<生成新的数据-----------------------------------------
	FInputKeyEvent temp;///<待添加的数据
	temp.Key = GroupKey.Key;
	temp.BIsMainKey = bIsMainKey;
	temp.KeyDatas.Empty();
	bool bHasAixs = false;
	bool bHasAction = false;
	for (auto& data : DefaultMainKey.KeyDatas)
	{
		if (data.Type == EINPUT_TYPE::IT_Axis)
		{
			if (GroupKey.Shift || GroupKey.Ctrl || GroupKey.Alt || GroupKey.Cmd)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(2605);
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("ChangeShortcutKeyData--->DefaultShortcutKeyData  Type is EINPUT_TYPE::IT_Axis and NewKey is GroupKey."));
				bIsSuccess = false;
				return ShortcutKey;
			}
			else
			{
				temp.KeyDatas = DefaultMainKey.KeyDatas;				
			}
			break;
		}

		if (data.Type == EINPUT_TYPE::IT_Action)
		{
			FInputKeyData tempdata;
			tempdata.Type = data.Type;
			tempdata.Scale = data.Scale;
			tempdata.Shift = GroupKey.Shift;
			tempdata.Ctrl = GroupKey.Ctrl;
			tempdata.Alt = GroupKey.Alt;
			tempdata.Cmd = GroupKey.Cmd;
			if (GroupKey.DoubleClick && ShortcutKey.CanDoubleClick)
			{
				tempdata.IE = EINPUT_EVENT::IE_DoubleClick;				
			}
			else if (data.IE == EINPUT_EVENT::IE_DoubleClick && !GroupKey.DoubleClick)
			{
				tempdata.IE = EINPUT_EVENT::IE_Pressed;
			}
			else
			{
				tempdata.IE = data.IE;
			}
			tempdata.FuncName = data.FuncName;
			temp.KeyDatas.Add(tempdata);
			bHasAction = true;
		}
		else
		{
			FInputKeyData tempdata;
			tempdata.Type = data.Type;
			tempdata.Scale = data.Scale;
			tempdata.Shift = data.Shift;
			tempdata.Ctrl = data.Ctrl;
			tempdata.Alt = data.Alt;
			tempdata.Cmd = data.Cmd;

			if (GroupKey.DoubleClick && ShortcutKey.CanDoubleClick)
			{
				tempdata.IE = EINPUT_EVENT::IE_DoubleClick;
			}
			else if (data.IE == EINPUT_EVENT::IE_DoubleClick && !GroupKey.DoubleClick)
			{
				tempdata.IE = EINPUT_EVENT::IE_Pressed;
			}
			else
			{
				tempdata.IE = data.IE;
			}
			tempdata.FuncName = data.FuncName;
			temp.KeyDatas.Add(tempdata);
			bHasAction = true;
			temp.KeyDatas.Add(data);
		}
	}
	if (!bHasAction && ShortcutKey.CanGroup &&(GroupKey.Shift || GroupKey.Ctrl || GroupKey.Alt || GroupKey.Cmd))
	{
		temp.KeyDatas.Reset();
		for (auto& keyDataInfo : DefaultMainKey.KeyDatas)
		{
			FInputKeyData tempdata;
			tempdata.Type = EINPUT_TYPE::IT_Action;
			tempdata.Scale = keyDataInfo.Scale;
			tempdata.Shift = GroupKey.Shift;
			tempdata.Ctrl = GroupKey.Ctrl;
			tempdata.Alt = GroupKey.Alt;
			tempdata.Cmd = GroupKey.Cmd;
			tempdata.IE = keyDataInfo.IE;
			tempdata.FuncName = keyDataInfo.FuncName;
			temp.KeyDatas.Add(tempdata);
		}
	}

	///<删除的数据------------------------------------
	if (!bIsAdd)
	{
		for (int i= 0;i<ShortcutKey.MainKey.Num();i++)
		{
			if (ShortcutKey.MainKey[i].Key == OldKey && ShortcutKey.MainKey[i].BIsMainKey == bIsMainKey)
			{
				//CS3_Display(CS3DebugType::CL_Undefined, TEXT("ChangeShortcutKeyData-->Remove ShortcutKey.MainKey[i]=%s"), *FNAME_TO_FSTRING(ShortcutKey.MainKey[i].Key.GetDisplayName()));
				ShortcutKey.MainKey.RemoveAt(i);
				break;
			}
		}
	}
	
	ShortcutKey.MainKey.Add(temp);
	bIsSuccess = true;
	//删除修改数据中已有的数据
	FSHORTCUTKEY tempShortcutData;
	RoleCtrlStateMgr->GetShortcutDataByActName(ShortcutKey.KeyType, ShortcutKey.ActName, tempShortcutData, true);
	RoleCtrlStateMgr->RemoveShortcutDataFromChangedKeys(tempShortcutData);
	//添加新修改的数据
	RoleCtrlStateMgr->AddShortcutDataToChangedKeys(ShortcutKey);
	ChangeShortcutKeyDataBP(OldShortcutKey, ShortcutKey);
	return ShortcutKey;
}

void ACS3PlayerController::GetShortcutDataByActName(SHORTCUTKEY_TYPE_ENUM KeyType, FName ActName, FSHORTCUTKEY& ShortcutData, bool bIsChangedKeys /*= false*/)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return	RoleCtrlStateMgr->GetShortcutDataByActName(KeyType, ActName, ShortcutData, bIsChangedKeys);
	}
}

bool ACS3PlayerController::ResetShortcutDataByKey(FSHORTCUTKEY ShortcutData, TArray<FKey>Keys, FSHORTCUTKEY& NewShortcutData)
{
	if (Keys.Num() < 1|| !ShortcutData.CanChange)return false;
	///<将Keys转换成FGROUPKEY_DATA类型
	FGROUPKEY_DATA GroupKey=UGolbalBPFunctionLibrary::ConvertKeysToGroupKey(Keys);
	
	RemoveBindInputData(ShortcutData.ActName, ShortcutData.MainKey);	

	FSHORTCUTKEY temp = ShortcutData;
	for (int i=0;i<temp.MainKey.Num();i++)
	{
		if (GroupKey.Key== temp.MainKey[i].Key)
		{
			for (auto InputKeyData : temp.MainKey[i].KeyDatas)
			{
				if (GroupKey.Alt == InputKeyData.Alt && GroupKey.Cmd == InputKeyData.Cmd && GroupKey.Ctrl == InputKeyData.Ctrl
					&& GroupKey.Shift == InputKeyData.Shift && GroupKey.DoubleClick == (InputKeyData.IE == EINPUT_EVENT::IE_DoubleClick))
				{
					ShortcutData.MainKey.RemoveAt(i);
					break;
				}
			}
			break;
		}		
	}
	NewShortcutData = ShortcutData;
	BindInputData(ShortcutData.ActName, ShortcutData.MainKey);
	if (IsValid(RoleCtrlStateMgr))
	{
		TArray<FSHORTCUTKEY> NewKeys;
		NewKeys.Add(ShortcutData);
		RoleCtrlStateMgr->SaveShortcutKeyDataToFile(NewKeys);
	}
	return true;
}

bool ACS3PlayerController::ResetChangedShortcutDataByKey(FSHORTCUTKEY ShortcutData, TArray<FKey>Keys, FSHORTCUTKEY& NewShortcutData)
{
	if (Keys.Num() < 1 || !ShortcutData.CanChange)return false;
	///<将Keys转换成FGROUPKEY_DATA类型
	FGROUPKEY_DATA GroupKey = UGolbalBPFunctionLibrary::ConvertKeysToGroupKey(Keys);
	FSHORTCUTKEY tempShortcutData;
	RoleCtrlStateMgr->GetShortcutDataByActName(ShortcutData.KeyType, ShortcutData.ActName, tempShortcutData, true);
	RoleCtrlStateMgr->RemoveShortcutDataFromChangedKeys(tempShortcutData);
	//添加新修改的数据
	FSHORTCUTKEY temp = ShortcutData;
	bool bIsMainKey = true;
	FInputKeyEvent KeyData;
	for (int i = 0; i < temp.MainKey.Num(); i++)
	{
		if (GroupKey.Key == temp.MainKey[i].Key)
		{
			for (auto InputKeyData : temp.MainKey[i].KeyDatas)
			{
				if (GroupKey.Alt == InputKeyData.Alt && GroupKey.Cmd == InputKeyData.Cmd && GroupKey.Ctrl == InputKeyData.Ctrl
					&& GroupKey.Shift == InputKeyData.Shift && GroupKey.DoubleClick == (InputKeyData.IE == EINPUT_EVENT::IE_DoubleClick))
				{
					KeyData = temp.MainKey[i];
					break;
				}
			}
			break;
		}
	}

	if (KeyData.Key.GetDisplayName().IsEmpty())
		return false;
	///<临时改变快捷键数据没有
	if (!tempShortcutData.ActName.Compare(""))
	{
		tempShortcutData = ShortcutData;
	}
	temp = tempShortcutData;
	for (int i = 0; i < temp.MainKey.Num(); i++)
	{
		if (temp.MainKey[i].BIsMainKey == KeyData.BIsMainKey)
		{
			tempShortcutData.MainKey.RemoveAt(i);
			break;
		}
	}

	RoleCtrlStateMgr->AddShortcutDataToChangedKeys(tempShortcutData);
	NewShortcutData = tempShortcutData;
	return true;
}

FString ACS3PlayerController::GetKeyNameByActName(FName ActName, FGROUPKEY_DATA& KeyValue)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return RoleCtrlStateMgr->GetKeyNameByActName(ActName, KeyValue);
	}
	return TEXT("");
}

bool ACS3PlayerController::IsKeyDownByActName(FName ActName)
{
	FGROUPKEY_DATA KeyValue;
	GetKeyNameByActName(ActName, KeyValue);
	if (GetInputKeyTimeDown(KeyValue.Key) > 0.0f)
	{
		if (KeyValue.Shift)
		{
			if (GetInputKeyTimeDown(EKeys::LeftShift) > 0.0f || GetInputKeyTimeDown(EKeys::RightShift) > 0.0f)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		else if (KeyValue.Alt)
		{
			if (GetInputKeyTimeDown(EKeys::LeftAlt) > 0.0f || GetInputKeyTimeDown(EKeys::RightAlt)>0.0f)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		else if (KeyValue.Cmd)
		{
			if (GetInputKeyTimeDown(EKeys::LeftCommand) > 0.0f || GetInputKeyTimeDown(EKeys::RightCommand) > 0.0f)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		else if (KeyValue.Ctrl)
		{
			if (GetInputKeyTimeDown(EKeys::LeftControl) > 0.0f || GetInputKeyTimeDown(EKeys::RightControl)>0.0f)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		return true;
	}
	return false;
}

TArray<FSHORTCUTKEY> ACS3PlayerController::GetShortcutDataByGroupKey(FKey Key)
{
	if (IsValid(RoleCtrlStateMgr))
	{
		return RoleCtrlStateMgr->GetShortcutDataByGroupKey(Key);
	}
	return TArray<FSHORTCUTKEY>();
}

bool ACS3PlayerController::CheckKeyExecutedByActionKey(FKey Key)
{
	TArray<FSHORTCUTKEY> ShortcutKeys = GetShortcutDataByGroupKey(Key);

	for (auto& ShortcutData : ShortcutKeys)
	{
		for (auto& ShortcuMainKey : ShortcutData.MainKey)
		{
			if (WasKeyJustPressedOrReleased(ShortcuMainKey.Key))
			{
				return true;
			}
		}
	}

	return false;
}

void ACS3PlayerController::BindInputData(FName ActName, TArray<FInputKeyEvent> KeyEvents)
{
	if (IsValid(InputComponent))
	{
		int Index = -1;
		const UInputSettings* InputSettings = GetDefault<UInputSettings>();
		for (auto& KeyEvent : KeyEvents)
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("BindInputData-->KeyEvent.GetDisplayName=%s"), *FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()));
			if (FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()) == "")
				continue;			
			Index++;
			for (auto& KeyData : KeyEvent.KeyDatas)
			{
				switch (KeyData.Type)
				{
				case EINPUT_TYPE::IT_Key:
				{
					/** BIND Key */
					if ((KeyEvents.Num() > 1 && Index == (KeyEvents.Num() - 1)) || KeyEvents.Num() == 1)
					{
						FInputKeyBinding KB(KeyEvent.Key, (EInputEvent)KeyData.IE);
						KB.KeyDelegate.BindDelegate(this, KeyData.FuncName);
						InputComponent->KeyBindings.Add(KB);
					}
					//InputComponent->BindKey();
				}break;
				case EINPUT_TYPE::IT_Action:
				{
					const FInputActionKeyMapping turnactionmapping(ActName, KeyEvent.Key, KeyData.Shift, KeyData.Ctrl, KeyData.Alt, KeyData.Cmd);
					((UInputSettings*)InputSettings)->AddActionMapping(turnactionmapping);
					((UInputSettings*)InputSettings)->SaveKeyMappings();

					/** BIND Action */
					if ((KeyEvents.Num() > 1 && Index == (KeyEvents.Num() - 1)) || KeyEvents.Num() == 1)
					{
						FInputActionBinding AB(ActName, (EInputEvent)KeyData.IE);
						AB.ActionDelegate.BindDelegate(this, KeyData.FuncName);
						InputComponent->AddActionBinding(AB);
						//CS3_Display(CS3DebugType::CL_Undefined, TEXT("IT_Action -> Exec KeyName[%s], ActName[%s]"), *FNAME_TO_FSTRING(KeyEvent.Key.GetFName()), *FNAME_TO_FSTRING(ActName));
					}
				}break;
				case EINPUT_TYPE::IT_Axis:
				{
					const FInputAxisKeyMapping turnaxismapping(ActName, KeyEvent.Key, KeyData.Scale);
					((UInputSettings*)InputSettings)->AddAxisMapping(turnaxismapping);
					((UInputSettings*)InputSettings)->SaveKeyMappings();

					/** BIND Axis */
					if ((KeyEvents.Num() > 1 && Index == (KeyEvents.Num() - 1)) || KeyEvents.Num() == 1)
					{
						FInputAxisBinding AB(ActName);
						AB.AxisDelegate.BindDelegate(this, KeyData.FuncName);
						InputComponent->AxisBindings.Add(AB);
					}
					//CS3_Display(CS3DebugType::CL_Undefined, TEXT("IT_Axis -> Exec KeyName[%s], AxisValue[%d]"), *FNAME_TO_FSTRING(KeyEvent.Key.GetFName()), KeyData.Scale);
					//InputComponent->BindAxis();
				}break;
				case EINPUT_TYPE::IT_AxisKey:
				{
					/** BIND AxisKey */
					if ((KeyEvents.Num() > 1 && Index == (KeyEvents.Num() - 1)) || KeyEvents.Num() == 1)
					{
						FInputAxisKeyBinding AB(KeyEvent.Key);
						//CS3_Display(CS3DebugType::CL_Undefined, TEXT("IT_AxisKey -> Exec KeyName[%s], AxisValue[%d]"), *FNAME_TO_FSTRING(KeyEvent.Key.GetFName()), KeyData.Scale);
						AB.AxisDelegate.BindDelegate(this, KeyData.FuncName);
						InputComponent->AxisKeyBindings.Add(AB);
					}
					//InputComponent->BindAxisKey();
				}break;
				}
			}
		}
	}
}

void ACS3PlayerController::RemoveBindInputData(FName ActName, TArray<FInputKeyEvent> KeyEvents)
{
	const UInputSettings* InputSettings = GetDefault<UInputSettings>();
	for (auto& KeyEvent : KeyEvents)
	{
		for (auto& KeyData : KeyEvent.KeyDatas)
		{
			switch (KeyData.Type)
			{
			case EINPUT_TYPE::IT_Key:
			{
				for (int i = 0; i < InputComponent->KeyBindings.Num(); i++)
				{
					FInputKeyBinding AB = InputComponent->KeyBindings[i];

					if (AB.Chord == KeyEvent.Key && AB.KeyEvent == (EInputEvent)KeyData.IE)
					{
						InputComponent->KeyBindings.RemoveAt(i);
						//CS3_Display(CS3DebugType::CL_Undefined, TEXT("~KeyBindings-------------- Key[%s]"), *FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()));
					}
				}

			}break;
			case EINPUT_TYPE::IT_Action:
			{
				const FInputActionKeyMapping turnactionmapping(ActName, KeyEvent.Key, KeyData.Shift, KeyData.Ctrl, KeyData.Alt, KeyData.Cmd);

				if (((UInputSettings*)InputSettings)->ActionMappings.Contains(turnactionmapping))
				{
					((UInputSettings*)InputSettings)->RemoveActionMapping(turnactionmapping);
				}

				for (int i = 0; i < InputComponent->GetNumActionBindings(); i++)
				{
					FInputActionBinding AB = InputComponent->GetActionBinding(i);

					if (AB.GetActionName() == ActName && AB.KeyEvent == (EInputEvent)KeyData.IE)
					{
						InputComponent->RemoveActionBinding(i);
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("~RemoveActionBinding--------------ActName=[%s]      Key[%s]"), *FNAME_TO_FSTRING(ActName), *FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()));
					}
				}

			}break;
			case EINPUT_TYPE::IT_Axis:
			{
				const FInputAxisKeyMapping turnaxismapping(ActName, KeyEvent.Key, KeyData.Scale);

				for (int i = 0; i < InputComponent->AxisBindings.Num(); i++)
				{
					FInputAxisBinding AB = InputComponent->AxisBindings[i];

					if (AB.AxisName == ActName)
					{
						InputComponent->AxisBindings.RemoveAt(i);
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("~RemoveAxisMapping--------------AxisName=[%s]     Key[%s]"), *FNAME_TO_FSTRING(ActName), *FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()));
					}
				}

				if (((UInputSettings*)InputSettings)->AxisMappings.Contains(turnaxismapping))
				{
					((UInputSettings*)InputSettings)->RemoveAxisMapping(turnaxismapping);				

				}
			}break;
			case EINPUT_TYPE::IT_AxisKey:
			{
				for (int i = 0; i < InputComponent->AxisKeyBindings.Num(); i++)
				{
					FInputAxisKeyBinding AB = InputComponent->AxisKeyBindings[i];

					if (AB.AxisKey == KeyEvent.Key)
					{
						InputComponent->AxisKeyBindings.RemoveAt(i);
						//CS3_Display(CS3DebugType::CL_Undefined, TEXT("~AxisKeyBindings------------- Key[%s]"), *FNAME_TO_FSTRING(KeyEvent.Key.GetDisplayName()));
					}
				}
			}break;
			}
		}
	}
}
void ACS3PlayerController::ChangeBindShortcutKeyByControlMode(ECONTROL_MODE NewType, ECONTROL_MODE OldType)
{
	if (NewType == OldType)return;

	TArray<FSHORTCUTKEY> ShortcutKeyData;
	if (OldType== ECONTROL_MODE::ActionControlMode)
	{
		ShortcutKeyData =RoleCtrlStateMgr->GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM::ACTMAINQUICKBAR);
	}
	else if (OldType == ECONTROL_MODE::DefaultControlMode)
	{
		ShortcutKeyData = RoleCtrlStateMgr->GetShortcutKeyDataByType(SHORTCUTKEY_TYPE_ENUM::NORMALMAINQUICKBAR);
	}
	if (NewType == ECONTROL_MODE::ActionControlMode)
	{
		ApplyShortcutKeyData(SHORTCUTKEY_TYPE_ENUM::ACTMAINQUICKBAR, ShortcutKeyData);
	}
	else if(NewType == ECONTROL_MODE::DefaultControlMode)
	{
		ApplyShortcutKeyData(SHORTCUTKEY_TYPE_ENUM::NORMALMAINQUICKBAR, ShortcutKeyData);
	}
}

bool ACS3PlayerController::BindKey_AnyKey_Pressed_Implementation(FKey Key)
{
	if (UUECS3GameInstance::Instance->QTEManager->OnKeyInputEvent.IsBound())
	{
		UUECS3GameInstance::Instance->QTEManager->OnKeyInputEvent.Broadcast(Key);
	}
	return CheckBindKeyActive(Key);
}

bool ACS3PlayerController::BindKey_AnyKey_Released_Implementation(FKey Key)
{
	return CheckBindKeyActive(Key);
}

const UConfigTable* ACS3PlayerController::GetInputConfig()
{
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager)
	{
		return UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_INPUT);
	}
	return nullptr;
}

const FINPUT_DATA* ACS3PlayerController::GetInputData(const FString& Id)
{
	const UConfigTable* InputConfig = GetInputConfig();
	return (IsValid(InputConfig)) ? InputConfig->GetRow<FINPUT_DATA>(Id) : nullptr;
}

FString ACS3PlayerController::GetKeyName(FKey Key)
{
	return FTEXT_TO_FSTRING(Key.GetDisplayName());
}

bool ACS3PlayerController::CheckContainsKey(FKey Key, TArray<FString> Keys)
{
	if (Keys.Contains(GetKeyName(Key)))
	{
		return true;
	}
	return false;
}

bool ACS3PlayerController::CheckBindKeyActive(FKey Key)
{
	bool IsActive = true;
	if (IsValid(RoleCtrlStateMgr))
	{
		for (auto& CtrlState : RoleCtrlStateMgr->GetCtrlStateList())
		{
			if(!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckKeyActive(Key);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool ACS3PlayerController::CheckBindActionActive(FName Name)
{
	bool IsActive = true;
	if (IsValid(RoleCtrlStateMgr))
	{
		for (auto& CtrlState : RoleCtrlStateMgr->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckActionActive(Name);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool ACS3PlayerController::CheckBindAxisActive(FName Name)
{
	bool IsActive = true;
	if (IsValid(RoleCtrlStateMgr))
	{
		for (auto& CtrlState : RoleCtrlStateMgr->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckAxisActive(Name);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}

bool ACS3PlayerController::CheckBindAxisKeyActive(FKey Key)
{
	bool IsActive = true;
	if (IsValid(RoleCtrlStateMgr))
	{
		for (auto& CtrlState : RoleCtrlStateMgr->GetCtrlStateList())
		{
			if (!IsValid(CtrlState)) continue;
			IsActive = IsActive && CtrlState->CheckAxisKeyActive(Key);
			// 有不激活状态即返回
			if (!IsActive) return false;
		}
	}
	return true;
}


bool ACS3PlayerController::CheckKeyDuration(FKey Key, float time)
{
	float TimeSeconds = GetWorld()->GetRealTimeSeconds();
	FKeyState* KeyState = UGolbalBPFunctionLibrary::GetCS3PlayerController()->PlayerInput->GetKeyState(Key);
	if (KeyState&& (TimeSeconds - KeyState->LastUpDownTransitionTime) > time)
	{
		return true;
	}
	return false;
}

bool ACS3PlayerController::WasKeyJustPressedOrReleased(FKey Key) const
{
	UWorld* World = GetWorld();
	if (IsValid(World) && IsValid(PlayerInput))
	{
		if (PlayerInput->IsPressed(Key)||PlayerInput->WasJustReleased(Key) || PlayerInput->WasJustPressed(Key))
		{
			return true;
		}
		FKeyState* KeyState = PlayerInput->GetKeyState(Key);
		float TimeSeconds = World->GetRealTimeSeconds();
		if (KeyState && (TimeSeconds - KeyState->LastUpDownTransitionTime) < 0.5)
		{
			return true;
		}
	}
	return false;
}

bool ACS3PlayerController::WasAltJustPressedOrReleased() const
{
	return WasKeyJustPressedOrReleased(EKeys::LeftAlt) || WasKeyJustPressedOrReleased(EKeys::RightAlt);
}

bool ACS3PlayerController::WasCtrlJustPressedOrReleased() const
{
	return WasKeyJustPressedOrReleased(EKeys::LeftControl) || WasKeyJustPressedOrReleased(EKeys::RightControl);
}

bool ACS3PlayerController::WasShiftJustPressedOrReleased() const
{
	return  WasKeyJustPressedOrReleased(EKeys::LeftShift) || WasKeyJustPressedOrReleased(EKeys::RightShift);
}

bool ACS3PlayerController::WasCmdJustPressedOrReleased() const
{	
	return WasKeyJustPressedOrReleased(EKeys::LeftCommand) || WasKeyJustPressedOrReleased(EKeys::RightCommand);
}

void ACS3PlayerController::KeepForward()
{
	//获取玩家
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//获取摄像机
	UCameraComponent* PlayerCamera = PlayerCharacter->CameraComponent;
	FVector CamLoaction = PlayerCamera->GetComponentLocation();
	//获取摄像机前方向
	FVector ForwardVec = PlayerCamera->GetForwardVector();

	//计算玩家朝向
	FVector EndLocation = FVector(CamLoaction.X + ForwardVec.X, CamLoaction.Y + ForwardVec.Y, CamLoaction.Z);

	FRotator RotaValue = UKismetMathLibrary::FindLookAtRotation(CamLoaction, EndLocation);

	PlayerCharacter->GetCapsuleComponent()->SetRelativeRotation(RotaValue);
}

void ACS3PlayerController::OnStopJumping()
{
	AServerCharacter* MyCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(MyCharacter))
	{
		MyCharacter->StopJumping();
	}
}

void ACS3PlayerController::RecordValueOfInputAxis(float Scale)
{
	Count++;
	if (Count > 3)
	{
		Count = 0;
		WScale = 0.0f;
	}
	else
	{
		if (!FMath::IsNearlyZero(Scale))
		{
			WScale = Scale;
		}
	}
}

void ACS3PlayerController::OnTurnWASDPressed(FString ActionName, FString InputKey)
{
	if (CheckBindActionActive(FSTRING_TO_FNAME(ActionName)))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ChangeControlModeFromACTToALT(false);
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(ActionName, InputKey, 0.0f, OtherValue);
			BP_OnWSADKeyPressed();
		}
	}
}

void ACS3PlayerController::OnUpdateWindow(FName ActionName, TArray<FString> OtherValue)
{
	if (CheckBindActionActive(ActionName))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("UpdateWindow"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnPlayerMoveTypeChanged(CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType)
{
	USkillInterface* RoleSkillInst = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
	if (IsValid(RoleSkillInst))
	{
		RoleSkillInst->OnMoveTypeChange(NewMoveType, OldMoveType);
	}
	URoleSpaceContentInterface* RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface"), 0));
	if (IsValid(RoleSpaceContentInterface))
	{
		RoleSpaceContentInterface->OnPlayerMoveTypeChange(NewMoveType, OldMoveType);
	}
	///<重置鼠标点击移动状态
	if (NewMoveType == CS3_MOVE_TYPE::MOVE_TYPE_NONE && (OldMoveType == CS3_MOVE_TYPE::MOVE_TYPE_FLY || OldMoveType == CS3_MOVE_TYPE::MOVE_TYPE_MOUSE))
	{
		bIsMouseClickNavMove = false;
	}
	if (NewMoveType == CS3_MOVE_TYPE::MOVE_TYPE_CONTROL && IsFlying()
		&& IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())
		&& IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetCharacterMovement()))
	{
		UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetCharacterMovement()->StopMovementImmediately();
	}
	///<移动模式改变，中断跟随
	if (!(NewMoveType == CS3_MOVE_TYPE::MOVE_TYPE_NONE || NewMoveType == CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW))
	{
		URoleTeamInterface* RoleTeamInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.RoleTeamInterface : nullptr;
		if (IsValid(RoleTeamInterface) && RoleTeamInterface->IsNormalFollowing())
		{
			RoleTeamInterface->cancelNormalFollowFC();
		}
	}
}

float ACS3PlayerController::GetMouseMoveScale()
{
	float Scale = 1.0f;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager) && IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData))
	{		
		bool IsMouseXDown = IsInputKeyDown(EKeys::LeftMouseButton);
		bool IsMouseYDown = IsInputKeyDown(EKeys::RightMouseButton);
		if (IsMouseXDown || IsMouseYDown)
		{
			Scale = UGolbalBPFunctionLibrary::GetMouseMoveSpeed() * UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.CameraTurnSpeed;
		}
		else
		{
			Scale = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.CameraTurnSpeed;
		}

	}
	return Scale;
}

void ACS3PlayerController::ClearInputEvent(AActor* Obj, bool bClearAll, EINPUT_TYPE Type)
{
	if (!IsValid(Obj)) return;

	if (bClearAll)
	{
		Obj->InputComponent->ClearActionBindings();
		Obj->InputComponent->KeyBindings.Reset();
		Obj->InputComponent->AxisBindings.Reset();
		Obj->InputComponent->AxisKeyBindings.Reset();
	}
	else
	{
		switch (Type)
		{
		case EINPUT_TYPE::IT_Action:
		{
			Obj->InputComponent->ClearActionBindings();
		}break;
		case EINPUT_TYPE::IT_Key:
		{
			Obj->InputComponent->KeyBindings.Reset();
		}break;
		case EINPUT_TYPE::IT_Axis:
		{
			Obj->InputComponent->AxisBindings.Reset();
		}break;
		case EINPUT_TYPE::IT_AxisKey:
		{
			Obj->InputComponent->AxisKeyBindings.Reset();
		}break;
		}
	}
}

void ACS3PlayerController::EnableInputToControll(bool IsCanInput)
{
	if (IsCanInput)
	{
		EnableInput(this);
	}
	else
	{
		DisableInput(this);
	}
}

int32 ACS3PlayerController::SetCameraRotateScale(float ScaleValue, int32 ScaleHeadle /*= -1*/)
{
	if (IsHaveCameraHeadle(ScaleHeadle))
	{
		//设置新值
		CameraRotateScales[ScaleHeadle] = ScaleValue;

		//刷新摄像机的旋转
		UpdataCameraRotateScale();

		return ScaleHeadle;
	}
	else
	{
		CameraRotateScaleCount++;
		CameraRotateScales.Add(CameraRotateScaleCount, ScaleValue);

		//刷新摄像机的旋转
		UpdataCameraRotateScale();

		return CameraRotateScaleCount;
	}
}

void ACS3PlayerController::UpdataCameraRotateScale()
{
	float ScaleValue = 1.0f;

	for (auto CameraScaleValue : CameraRotateScales)
	{
		ScaleValue *= CameraScaleValue.Value;
	}

	InputYawScale = fDefaultCameraRotateScale * ScaleValue;
}

bool ACS3PlayerController::RemoveCameraRotateScale(int32 ScaleHeadle)
{
	if (IsHaveCameraHeadle(ScaleHeadle))
	{
		//设置新值
		CameraRotateScales.Remove(ScaleHeadle);

		//刷新摄像机的旋转
		UpdataCameraRotateScale();

		return true;
	}
	else
	{
		return false;
	}
}

bool ACS3PlayerController::IsHaveCameraHeadle(int32 ScaleHeadle)
{
	return CameraRotateScales.Contains(ScaleHeadle);
}

void ACS3PlayerController::AddMovementArray(FVector InputVector, float axis)
{
	if (IsFlying() && IsValid(UGolbalBPFunctionLibrary::MapManager()) && UGolbalBPFunctionLibrary::MapManager()->IsPlayerFlyCeiling())
	{
		if (InputVector.Z > 0.0f)
		{
			InputVector = FVector(InputVector.X, InputVector.Y, 0.0f);
		}
	}
	MovementInputs.Add(InputVector * axis);
}

class AGameCharacter* ACS3PlayerController::GetPlayerCharacterProxy()
{
	if (!IsValid(PlayerCharacterProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("PlayerCharacterProxy"));
		PlayerCharacterProxy = Cast<AGameCharacter>(actor);
	}
	return PlayerCharacterProxy;
}

class AGameCharacter* ACS3PlayerController::GetPlayerTargetProxy()
{
	if (!IsValid(PlayerTargetProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("PlayerTargetProxy"));
		PlayerTargetProxy = Cast<AGameCharacter>(actor);
	}
	return PlayerTargetProxy;
}

class AGameCharacter* ACS3PlayerController::GetRoleModelProxy()
{
	if (!IsValid(RoleModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("RoleModelProxy"));
		RoleModelProxy = Cast<AGameCharacter>(actor);
	}
	return RoleModelProxy;
}

class AGameCharacter* ACS3PlayerController::GetPetModelProxy()
{
	if (!IsValid(PetModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("PetModelProxy"));
		PetModelProxy = Cast<AGameCharacter>(actor);
	}
	return PetModelProxy;
}

class AGameCharacter* ACS3PlayerController::GetPetPenModelProxy()
{
	if (!IsValid(PetPenModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("PetPenModelProxy"));
		PetPenModelProxy = Cast<AGameCharacter>(actor);
	}
	return PetPenModelProxy;
}

class AGameCharacter* ACS3PlayerController::GetHalfHeadModelProxy()
{
	if (!IsValid(HalfHeadModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("HalfHeadModelProxy"));
		HalfHeadModelProxy = Cast<AGameCharacter>(actor);
		UGolbalBPFunctionLibrary::AddCameraHiddenActor(HalfHeadModelProxy);
	}
	return HalfHeadModelProxy;
}

AGameCharacter * ACS3PlayerController::GetRoleHalfHeadModelProxy()
{
	if (!IsValid(RoleHalfHeadModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("RoleHalfHeadModelProxy"));
		RoleHalfHeadModelProxy = Cast<AGameCharacter>(actor);
	}
	return RoleHalfHeadModelProxy;
}

class AGameCharacter* ACS3PlayerController::GetOtherRoleModelProxy()
{
	if (!IsValid(OtherRoleModelProxy))
	{
		AActor* actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("RoleModelProxy"));
		OtherRoleModelProxy = Cast<AGameCharacter>(actor);
	}
	return OtherRoleModelProxy;
}

class AGameCharacter* ACS3PlayerController::GetTongNagualModelProxy()
{
	if (!IsValid(TongNagualModelProxy))
	{
		AActor* Actor = UGolbalBPFunctionLibrary::SpawnActorByConfig(this, TEXT("TongNagualModelProxy"));
		TongNagualModelProxy = Cast<AGameCharacter>(Actor);
	}
	return TongNagualModelProxy;
}

void ACS3PlayerController::OnDodgeFront()
{
	if (!CheckBindActionActive(TEXT("DodgeFront")))return;
	
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("DodgeFront"), TEXT(""), 0.0f, OtherValue);
	}
	else
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnDodgeFront --- ControllerModeMgr Is Null !"));
	}
}

void ACS3PlayerController::OnDodgeBack()
{
	if (!CheckBindActionActive(TEXT("DodgeBack")))return;

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("DodgeBack"), TEXT(""), 0.0f, OtherValue);
	}
	else
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnDodgeBack --- ControllerModeMgr Is Null !"));
	}
}

void ACS3PlayerController::OnDodgeLeft()
{
	if (!CheckBindActionActive(TEXT("DodgeLeft")))return;

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("DodgeLeft"), TEXT(""), 0.0f, OtherValue);
	}
	else
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnDodgeLeft --- ControllerModeMgr Is Null !"));
	}
}

void ACS3PlayerController::OnDodgeRight()
{
	if (!CheckBindActionActive(TEXT("DodgeRight")))return;

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;
		ControllerModeMgr->ExecuteInputInfor(TEXT("DodgeRight"), TEXT(""), 0.0f, OtherValue);
	}
	else
	{
		CS3_Warning(TEXT("ACS3PlayerController::OnDodgeRight --- ControllerModeMgr Is Null !"));
	}
}

void ACS3PlayerController::OnMoveForward(float Scale)
{
	if (CheckBindAxisActive(TEXT("MoveForward")))
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		RecordValueOfInputAxis(Scale);
		TArray<FString> OtherValue;

		if (IsValid(PlayerCharacter) && PlayerCharacter->IsLadderMovement())
		{
			if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
			{
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("LadderMoveForward"), TEXT(""), Scale, OtherValue);
			}
		}
		else
		{
			if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
			{
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MoveForward"), TEXT(""), Scale, OtherValue);
			}
		}
	}
}

void ACS3PlayerController::OnMoveRight(float Scale)
{
	if (CheckBindAxisActive(TEXT("MoveRight")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MoveRight"), TEXT(""), Scale, OtherValue);
		}
	}
}

void ACS3PlayerController::OnLookUp(float Scale)
{
	if (CheckBindAxisActive(TEXT("LookUp")))
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (PlayerCharacter)
		{
			float PitchValue = PlayerCharacter->CameraComponent->GetComponentRotation().Pitch;
			float MouseMoveScale = GetMouseMoveScale();
			if ((Scale > 0.0f && (PitchValue + MouseMoveScale * Scale*InputPitchScale) > UpAngle) || (Scale < 0.0f && (PitchValue + MouseMoveScale * Scale*InputPitchScale) < DownAngle))
			{
				if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
				{
					TArray<FString> OtherValue;
					UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("LookUp"), TEXT(""), Scale, OtherValue);
				}
			}
		}
	}
}

void ACS3PlayerController::OnTurn(float Scale)
{
	if (CheckBindAxisActive(TEXT("Turn")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("Turn"), TEXT(""), Scale, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMoveUp(float Scale)
{
	if (CheckBindAxisActive(TEXT("MoveUp")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MoveUp"), TEXT(""), Scale, OtherValue);
		}
	}
}

void ACS3PlayerController::OnTurnForwardReleased(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("TurnForwardReleased"), TEXT("W"), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnTurnBackReleased(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("TurnBackReleased"), TEXT("S"), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnTurnLeftReleased(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("TurnLeftReleased"), TEXT("A"), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnTurnRightReleased(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("TurnRightReleased"), TEXT("D"), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnTurnForwardPressed(FKey Key)
{
	OnTurnWASDPressed(TEXT("TurnForwardPressed"), TEXT("W"));
}

void ACS3PlayerController::OnTurnBackPressed(FKey Key)
{
	OnTurnWASDPressed(TEXT("TurnBackPressed"), TEXT("S"));
}

void ACS3PlayerController::OnTurnLeftPressed(FKey Key)
{
	OnTurnWASDPressed(TEXT("TurnLeftPressed"), TEXT("A"));
}

void ACS3PlayerController::OnTurnRightPressed(FKey Key)
{
	OnTurnWASDPressed(TEXT("TurnRightPressed"), TEXT("D"));
}

void ACS3PlayerController::OnSetTarget(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedEnemy")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(1));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectSelf(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedSelf")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(2));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectTeammate1(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedTeammate1")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(3));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectTeammate2(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedTeammate2")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(4));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectTeammate3(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedTeammate3")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(5));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectTeammate4(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedTeammate4")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(6));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSelectTargetToTarget(FKey Key)
{
	if (CheckBindActionActive(TEXT("SelectedTargetToTarget")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(7));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("SelectTarget"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnInteractive(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("Interactive"), TEXT(""), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnUsePrompet(FKey Key)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		URolePerformanceInterface* RolePerformanceInterface = Cast<URolePerformanceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface"), 0));
		FString PrompetID;
		if (IsValid(RolePerformanceInterface))
		{
			if (RolePerformanceInterface->PrompetItemID != 0)
			{
				TArray<FString> OtherValue = { "",FString::FromInt(RolePerformanceInterface->PrompetItemID) };
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("UseItemInQuick"), TEXT(""), 0.0f, OtherValue);
			}
			else if(RolePerformanceInterface->PrompetskillID != 0)
			{
				TArray<FString> OtherValue = { FString::FromInt(RolePerformanceInterface->PrompetskillID), FString::FromInt(UGolbalBPFunctionLibrary::GetTargetEntityID()) };
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("UseSkill"), TEXT(""), 0.0f, OtherValue);
			}
		}
	}
}

void ACS3PlayerController::OnSwitchControlPlayer()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		APlayerCharacter* CurPlayerTarget = Cast<APlayerCharacter>(PlayerCharacter->CurPlayerTarget);
		if (IsValid(CurPlayerTarget))
		{
			CurPlayerTarget->SwitchControlToSelf();
		}
	}
}

bool ACS3PlayerController::OnEscPressed_Implementation()
{
	return true;
}

void ACS3PlayerController::ChangeControlModeFromACTToALT(bool bIsActToAlt)
{
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ChangeControlModeFromACTToALT(bIsActToAlt);
	}
}

void ACS3PlayerController::OnUpdatePlayerModlevisible()
{
	if (CheckBindActionActive(TEXT("UpdatePlayerModlevisible")))
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(PlayerCharacter)&&IsValid(UGolbalBPFunctionLibrary::VisibleManager()))
		{
			UGolbalBPFunctionLibrary::VisibleManager()->UpdateModelVisible(PlayerCharacter);
		}
	}
}

void ACS3PlayerController::OnVehicle()
{
	if (CheckBindActionActive(TEXT("Vehicle")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("Vehicle"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnAutoForward()
{
	if (CheckBindActionActive(TEXT("AutoForward")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ChangeControlModeFromACTToALT(false);

			if (IsValid(UGolbalBPFunctionLibrary::OperationModeMgr()))
			{
				TArray<FString> OtherValue;
				if (UGolbalBPFunctionLibrary::OperationModeMgr()->bIsAutoMove)
				{
					UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("CloseAutoForward"), TEXT(""), 0.0f, OtherValue);
				}
				else
				{
					UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("OpenAutoForward"), TEXT(""), 0.0f, OtherValue);
				}				
			}
		}
	}
}

void ACS3PlayerController::OnPrintScreen()
{
	if (CheckBindActionActive(TEXT("Screenshot")))
	{
		UKismetSystemLibrary::ExecuteConsoleCommand(this, TEXT("shot"));
	}
}

void ACS3PlayerController::OnMouseScrollBig()
{
	if (CheckBindActionActive(TEXT("MouseScrollBig")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseScrollBig"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMouseScrollSmall()
{
	if (CheckBindActionActive(TEXT("MouseScrollSmall")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseScrollSmall"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMouseLeftPressed(FKey Key)
{
	if (CheckBindKeyActive(Key))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseLeftPressed"), GetKeyName(Key), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMouseLeftReleased(FKey Key)
{
	if (CheckBindKeyActive(Key))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseLeftReleased"), GetKeyName(Key), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMouseRightPressed(FKey Key)
{
	if (CheckBindKeyActive(Key))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseRightPressed"), GetKeyName(Key), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMouseRightReleased(FKey Key)
{
	if (CheckBindKeyActive(Key))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MouseRightReleased"), GetKeyName(Key), 0.0f, OtherValue);
		}
	}
}


void ACS3PlayerController::ActionModeMouseEvent()
{
	if (CheckBindActionActive(TEXT("ActionModeMouseEvent")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("ActionModeMouseEvent"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

bool ACS3PlayerController::UseQuickKey_Implementation(int32 ShortcutIndex, bool IsMainQuickKey/* = true*/)
{	
	return false;
}

bool ACS3PlayerController::BP_OnWSADKeyPressed_Implementation()
{
	return true;
}

void ACS3PlayerController::OnMainSkill0(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill0")))
	{
		//UseQuickKey(0);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(0));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill1(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill1")))
	{
		//UseQuickKey(1);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(1));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill2(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill2")))
	{
		//UseQuickKey(2);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(2));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill3(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill3")))
	{
		//UseQuickKey(3);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(3));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill4(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill4")))
	{
		//UseQuickKey(4);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(4));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill5(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill5")))
	{
		//UseQuickKey(5);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(5));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill6(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill6")))
	{
		//UseQuickKey(6);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(6));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill7(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill7")))
	{
		//UseQuickKey(7);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(7));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnMainSkill8(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill8")))
	{
		//UseQuickKey(8);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(8));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}
void ACS3PlayerController::OnMainSkill9(FKey Key)
{
	if (CheckBindActionActive(TEXT("MainSkill9")))
	{
		//UseQuickKey(9);
		if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
		{
			TArray<FString> OtherValue;
			OtherValue.Add(INT_TO_FSTRING(9));
			UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("MainSkill"), TEXT(""), 0.0f, OtherValue);
		}
	}
}

void ACS3PlayerController::OnSecondSkill0(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill10")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2 + 4;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill1(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill1")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill2(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill2")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1 + 1;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill3(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill3")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1 + 2;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill4(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill4")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1 + 3;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill5(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill5")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_1 + 4;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill6(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill6")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill7(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill7")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2 + 1;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill8(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill8")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2 + 2;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnSecondSkill9(FKey Key)
{
	if (CheckBindActionActive(TEXT("SecondSkill9")))
	{
		int32 Index = UUECS3GameInstance::Instance->ConstDataBP->QB_IDX_ROLE_ADDITIONAL_SHORTCUT_BAR_2 + 3;
		UseQuickKey(Index, false);
	}
}

void ACS3PlayerController::OnShiftKeyPressed()
{
	if (CheckBindActionActive(TEXT("ShiftKey")))
	{
		bIsShiftDown = true;
	}
}

void ACS3PlayerController::OnShiftkeyReleased()
{
	bIsShiftDown = false;
}

void ACS3PlayerController::OnCtrlKeyPressed()
{
	if (CheckBindActionActive(TEXT("CtrlKey")))
	{
		bIsCtrlDown = true;
	}
	if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
	{
		TArray<FString> OtherValue;
		UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("ShowSkillInfoTips"), TEXT(""), 0.0f, OtherValue);
	}
}

void ACS3PlayerController::OnCtrlKeyReleased()
{
	bIsCtrlDown = false;
}

void ACS3PlayerController::OnAltKeyPressed()
{
	if (CheckBindActionActive(TEXT("AltKey")))
	{
		bIsAltDown = true;
	}
}

void ACS3PlayerController::OnAltKeyReleased()
{
	bIsAltDown = false;
}

void ACS3PlayerController::OnMouseRightKeyPressed()
{
	if (CheckBindActionActive(TEXT("MouseRightKey")))
	{
		if (IsValid(UGolbalBPFunctionLibrary::CustomCursorManager()))
		{
			UGolbalBPFunctionLibrary::CustomCursorManager()->ResetCursor();
		}
	}
}

void ACS3PlayerController::OnShowActivityCalendarUI()
{
	TArray<FString> OtherValue = {"0","7","ActivityCalendar","0","0"};
	OnUpdateWindow(TEXT("ActivityCalendarUI"), OtherValue);
}

void ACS3PlayerController::OnShowFPSUI()
{
	TArray<FString> OtherValue = { "0","7","FPS","0","0" };
	OnUpdateWindow(TEXT("RunFPS"), OtherValue);
}

void ACS3PlayerController::OnShowBigMapUI()
{
	if (UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID")).Compare("fu_ben_L_BHZB_DBY") == 0)
	{
		URoleActivityInterface* activityInterface = Cast<URoleActivityInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleActivityInterface")));
		if (IsValid(activityInterface))
		{
			activityInterface->LoadBHZBPointCfgData(true);
		}
	}
	else if ((UGolbalBPFunctionLibrary::GetSpaceData(TEXT("SPACE_SCRIPT_ID")).Compare(TEXT("cycle_L_PSDBGZ"))))
	{
		TArray<FString> OtherValue = { "0","7","BigMap","0","0" };
		OnUpdateWindow(TEXT("MapUI"), OtherValue);
	}
	else
	{
		if (CheckBindActionActive(TEXT("MapUI")))
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(4053);
		}
	}	
}

void ACS3PlayerController::OnShowKitbagUI()
{
	TArray<FString> OtherValue = { "0","7","KitBag","0","0" };
	OnUpdateWindow(TEXT("BagUI"), OtherValue);
}

void ACS3PlayerController::OnShowEquipUI()
{
	TArray<FString> OtherValue = { "0","7","Equip","0","0" };
	OnUpdateWindow(TEXT("EquipUI"), OtherValue);
}

void ACS3PlayerController::OnShowQuestUI()
{
	TArray<FString> OtherValue = { "0","7","TaskList","0","0" };
	OnUpdateWindow(TEXT("QuestUI"), OtherValue);
}

void ACS3PlayerController::OnShowRolePertyUI()
{
	TArray<FString> OtherValue = { "0","7","RoleProperty","0","0" };
	OnUpdateWindow(TEXT("RolePropertyUI"), OtherValue);
}

void ACS3PlayerController::OnShowRelationUI()
{
	TArray<FString> OtherValue = { "0","7","Relation","0","0" };
	OnUpdateWindow(TEXT("RelationUI"), OtherValue);
}

void ACS3PlayerController::OnShowMemoirUI()
{
	TArray<FString> OtherValue = { "0","7","Memoir","0","0" };
	OnUpdateWindow(TEXT("MemoirUI"), OtherValue);
}

void ACS3PlayerController::OnShowTransportUI()
{
	TArray<FString> OtherValue = { "0","7","Transport","0","0" };
	OnUpdateWindow(TEXT("TransportU"), OtherValue);
}

void ACS3PlayerController::OnShowSkillUpgradeUI()
{
	TArray<FString> OtherValue = { "0","7","SkillUpgraded","0","0" };
	OnUpdateWindow(TEXT("SkillUI"), OtherValue);
}

void ACS3PlayerController::OnShowPetUI()
{
	TArray<FString> OtherValue = { "0","7","Pet","0","0" };
	OnUpdateWindow(TEXT("PetUI"), OtherValue);
}

void ACS3PlayerController::OnShowMallUI()
{
	TArray<FString> OtherValue = { "0","7","Mall","0","0" };
	OnUpdateWindow(TEXT("MallUI"), OtherValue);
}

void ACS3PlayerController::OnShowHelpSystemUI()
{
	TArray<FString> OtherValue = { "0","7","Help","0","0" };
	OnUpdateWindow(TEXT("HelpSystemUI"), OtherValue);
}

void ACS3PlayerController::OnCrtlAddOne()
{
	UseSpaceCopyItemByQuickKey(0);
}

void ACS3PlayerController::OnCrtlAddTwo()
{
	UseSpaceCopyItemByQuickKey(1);
}

void ACS3PlayerController::OnCrtlAddThree()
{
	UseSpaceCopyItemByQuickKey(2);
}

void ACS3PlayerController::OnCrtlAddFour()
{
	UseSpaceCopyItemByQuickKey(3);
}

void ACS3PlayerController::OnCrtlAddFive()
{
	UseSpaceCopyItemByQuickKey(4);
}

void ACS3PlayerController::OnCrtlAddSix()
{
	UseSpaceCopyItemByQuickKey(5);
}

void ACS3PlayerController::OnCrtlAddSeven()
{
	UseSpaceCopyItemByQuickKey(6);
}

void ACS3PlayerController::OnCrtlAddEight()
{
	UseSpaceCopyItemByQuickKey(7);
}

void ACS3PlayerController::UseSpaceCopyItemByQuickKey(const int32& index)
{
	URoleKitBagInterface* kitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (IsValid(kitBagInterface))
	{
		kitBagInterface->UseSpaceCopyItemByQuickKey(index);
	}
}

void ACS3PlayerController::SetUpAndDownAngle(float upAngle, float downAngle)
{
	UpAngle = FMath::Clamp(upAngle, -60.0f, 45.0f);
	DownAngle = FMath::Clamp(downAngle, -60.0f, 45.0f);
}

float ACS3PlayerController::GetWKeyScale()
{
	return WScale;
}

//=====//以下部分是技能测试功能用stand=======
void ACS3PlayerController::OnSkillAtkCeShi1()
{
}

void ACS3PlayerController::OnSkillAtkCeShi2()
{
}

void ACS3PlayerController::OnSkillAtkCeShi3()
{
}

AActor* ACS3PlayerController::CS3SpawnActor(UClass* Class, const FTransform& SpawnTransform, ESpawnActorCollisionHandlingMethod CollisionHandlingOverride)
{
	FActorSpawnParameters SpawnParameters;
	SpawnParameters.SpawnCollisionHandlingOverride = CollisionHandlingOverride;
	FVector Location = SpawnTransform.GetLocation();
	FRotator Ratation = FRotator(SpawnTransform.GetRotation());
	return UUECS3GameInstance::Instance->GetWorld()->SpawnActor(Class, &Location, &Ratation, SpawnParameters);
}

void ACS3PlayerController::OnResolutionChanged(FViewport* ViewPort, uint32 val)
{
	NewReso = ViewPort->GetSizeXY();
	if (NewReso.IsZero())
	{
		CS3_Warning(TEXT("-->error:ACS3PlayerController::OnResolutionChanged : ViewportSize IsZero !"));
	};
	UUECS3GameInstance::Instance->UIFixerManager->OnResolutionChanged(PreReso, PreScale, NewReso);
	UUECS3GameInstance::Instance->TutorialManager->OnResolutionChanged(PreReso, PreScale, NewReso);
	PreReso = NewReso;
	PreScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(PreReso.X, PreReso.Y));
}


void ACS3PlayerController::LoadPlayer()
{
}
void ACS3PlayerController::FlushPressedKeys()
{
	if (PlayerInput)
	{
		//保存清楚前状态
		for(auto &Item : FlushKeyStateMapSkip)
		{ 
			FKeyState *KeyState = PlayerInput->GetKeyState(Item.Key);
			if (KeyState)
			{
				Item.Value.RawValue = KeyState->RawValue;
				Item.Value.bDown = KeyState->bDown;
				Item.Value.bDownPrevious = KeyState->bDownPrevious;
				Item.Value.LastUpDownTransitionTime = KeyState->LastUpDownTransitionTime;
				KeyState->bDown = 0;
			}
		}

		PlayerInput->FlushPressedKeys();

		for(auto &Item : FlushKeyStateMapSkip)
		{ 
			FKeyState *KeyState = PlayerInput->GetKeyState(Item.Key);
			if (KeyState)
			{
				KeyState->RawValue = Item.Value.RawValue;
				KeyState->bDown = Item.Value.bDown;
				KeyState->bDownPrevious = Item.Value.bDownPrevious;
				KeyState->LastUpDownTransitionTime = Item.Value.LastUpDownTransitionTime;
			}
		}
	}
}






//=====//以下部分是技能测试功能用end=======
CONTROL_COMPILE_OPTIMIZE_END

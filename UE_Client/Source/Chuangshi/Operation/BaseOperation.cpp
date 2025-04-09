// Fill out your copyright notice in the Description page of Project Settings.


#include "BaseOperation.h"
#include "CS3Base/UIManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Kismet/KismetMathLibrary.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "WidgetBlueprintLibrary.h"
#include "Interface/SkillInterface.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Interface/Role/RoleStateInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemUse.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Manager/GameStatus.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/SpringArmComponentEX.h"
#include "GameFramework/PawnMovementComponent.h"
#include "GameFramework/PlayerInput.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/RootUIWidget.h" 
#include "Manager/MessageManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "GameData/MessageID.h"
#include "Manager/EventManager.h"
#include "GameData/GameDefault.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/AtkStateMar.h"
#include "Manager/CustomTimerManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Component/Role/JumpComponent.h"
#include "CS3Base/CS3UserWidget.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/Role/RoleStallInterface.h"
#include "Interface/Role/RoleInterface.h"
#include "Actor/Scene/MovingPlatformShipsCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "Actor/Monster/MonsterGhostEyeCharacter.h"
#include "UnrealMathUtility.h"
#include "NoExportTypes.h"
#include "Camera/PlayerCameraManager.h"
#include "GameData/ConstDataBP.h"
#include "Component/Role/FlyPatrolComponent.h"
#include "Interface/GameObjectInterface.h"
#include "CoreMiscDefines.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Interface/Role/RolePetInterface.h"
#include "Actor/Scene/MovingPlatformVehicleCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("UBaseMoveOperation_ExecuteOperation"), STAT_UBaseMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UFlyUpOperation_ExecuteOperation"), STAT_UFlyUpOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UKeepDirectionOperation_ExecuteOperation"), STAT_UKeepDirectionOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUnKeepDirectionOperation_ExecuteOperation"), STAT_UUnKeepDirectionOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("URecordPlayerVectorOperation_ExecuteOperation"), STAT_URecordPlayerVectorOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UShowMouseOperation_ExecuteOperation"), STAT_UShowMouseOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UHideMouseOperation_ExecuteOperation"), STAT_UHideMouseOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaseCameraTurn_ExecuteOperation"), STAT_UBaseCameraTurn_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UClearSkillAssisOperation_ExecuteOperation"), STAT_UClearSkillAssisOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UMoveByClickOperation_ExecuteOperation"), STAT_UMoveByClickOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UCallLeftClickEventOperation_ExecuteOperation"), STAT_UCallLeftClickEventOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UCameraBeOperationOperation_ExecuteOperation"), STAT_UCameraBeOperationOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUnCameraBeOperationOperation_ExecuteOperation"), STAT_UUnCameraBeOperationOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("USACTBaseTurnOperation_ExecuteOperation"), STAT_USACTBaseTurnOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UTurnOperation_ExecuteOperation"), STAT_UTurnOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UActionTurnOperation_ExecuteOperation"), STAT_UActionTurnOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UALTTurnOperation_ExecuteOperation"), STAT_UALTTurnOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UActorCanTurnOperation_ExecuteOperation"), STAT_UActorCanTurnOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UOpenAutoMoveOperation_ExecuteOperation"), STAT_UOpenAutoMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UCloseAutoMoveOperation_ExecuteOperation"), STAT_UCloseAutoMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaseDodgeOperation_ExecuteOperation"), STAT_UBaseDodgeOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaseFlexHandleOperation_ExecuteOperation"), STAT_UBaseFlexHandleOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaseFlexHandleOperation_ModelTurn_ExecuteOperation"), STAT_UBaseFlexHandleOperation_ModelTurn_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("USwitchToAltOperation_ExecuteOperation"), STAT_USwitchToAltOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UFlushPressedKeysOperation_ExecuteOperation"), STAT_UFlushPressedKeysOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("USwitchToYControlOperation_ExecuteOperation"), STAT_USwitchToYControlOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("URecoveryModeOperation_ExecuteOperation"), STAT_URecoveryModeOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UJumpPressedOperation_ExecuteOperation"), STAT_UJumpPressedOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UJumpReleasedOperation_ExecuteOperation"), STAT_UJumpReleasedOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("USwitchToDafaultQuickOperation_ExecuteOperation"), STAT_USwitchToDafaultQuickOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("USwitchToActionQuickOperation_ExecuteOperation"), STAT_USwitchToActionQuickOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UActorCanRotateOperation_ExecuteOperation"), STAT_UActorCanRotateOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UAdjustViewTargetWithBlendOperation_ExecuteOperation"), STAT_UAdjustViewTargetWithBlendOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUnAdjustViewTargetWithBlendOperation_ExecuteOperation"), STAT_UUnAdjustViewTargetWithBlendOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseSkillOperation_ExecuteOperation"), STAT_UUseSkillOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseSkillOperation_GetSkillIDByState"), STAT_UUseSkillOperation_GetSkillIDByState, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseItemBaseOperation_ExecuteOperation"), STAT_UUseItemBaseOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseItemInQuickOperation_ExecuteOperation"), STAT_UUseItemInQuickOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UCheckChangeToYOperation_ExecuteOperation"), STAT_UCheckChangeToYOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UHeHuaForwardMoveOperation_ExecuteOperation"), STAT_UHeHuaForwardMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UHeHuaBackwardsMoveOperation_ExecuteOperation"), STAT_UHeHuaBackwardsMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UHeHuaRightsMoveOperation_ExecuteOperation"), STAT_UHeHuaRightsMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UHeHuaLeftMoveOperation_ExecuteOperation"), STAT_UHeHuaLeftMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UDismountHeHuaOperation_ExecuteOperation"), STAT_UDismountHeHuaOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("URandomActionOperation_ExecuteOperation"), STAT_URandomActionOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseSkillOfShoot_ExecuteOperation"), STAT_UUseSkillOfShoot_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUseSkillOfLineShoot_ExecuteOperation"), STAT_UUseSkillOfLineShoot_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBreakSkillOfLineShoot_ExecuteOperation"), STAT_UBreakSkillOfLineShoot_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UActivateNavigateMoveMode_ExecuteOperation"), STAT_UActivateNavigateMoveMode_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UUnActivateNavigateMoveMode_ExecuteOperation"), STAT_UUnActivateNavigateMoveMode_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UStartCrossMapNavigate_ExecuteOperation"), STAT_UStartCrossMapNavigate_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaGuaZhenForwardMoveOperation_ExecuteOperation"), STAT_UBaGuaZhenForwardMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);
DECLARE_CYCLE_STAT(TEXT("UBaGuaZhenRightMoveOperation_ExecuteOperation"), STAT_UBaGuaZhenRightMoveOperation_ExecuteOperation, STATGROUP_UBaseOperation);


#pragma region	操作基类
void UBaseOperation::Init(FString OperName)
{
	m_OperName = OperName;
}

void UBaseOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	BP_ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UBaseOperation::IsCanExecuteOperation()
{
	if (!BP_IsCanExecuteOperation())
	{
		return false;
	}

	//判断玩家
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()))
	{
		return false;
	}

	return true;
}

bool UBaseOperation::BP_IsCanExecuteOperation_Implementation()
{
	return true;
}

#pragma endregion

#pragma region	移动操作基类
void UBaseMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerController)|| !IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseMoveOperation::ExecuteOperation : PlayerController !"));
			return;
	}
	if (!IsCanExecuteOperation())
	{
		if (!FMath::IsNearlyZero(InputScale))
		{
			if (IsValid(UUECS3GameInstance::Instance->MessageManager))
			{				
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(28);
			}
		}
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseMoveOperation::ExecuteOperation : OperationModeMgr!"));
		return;
	}

	FVector ForwardByPlayer = FVector::ZeroVector;
	FVector ForwardByFlyPlayer = FVector::ZeroVector;
	FVector KeepVector = FVector::ZeroVector;

	//获取移动向量数据
	if (!GetMoveVector(ForwardByPlayer, ForwardByFlyPlayer, KeepVector))
	{
		return;
	}

	//移动轴值记录
	float Scale = InputScale;

	//判断是否为自动移动
	if (OperationModeMgr->bIsAutoMove)
	{
		Scale = 1.0f;
	}

	//是否保持方向不变
	if (OperationModeMgr->bIsKeepDirection)
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(KeepVector, Scale);
	}
	else if (PlayerController->IsFlying())//飞行状态
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(ForwardByFlyPlayer, Scale);
	}
	else
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(ForwardByPlayer, Scale);
	}
}

bool UBaseMoveOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	return true;
}

bool UBaseMoveOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		CS3_Log(TEXT("UBaseMoveOperation::IsCanExecuteOperation : Super::IsCanExecuteOperation() return false!"));
		return false;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//不能移动则禁用
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	APlayerCharacter* PlayerActor =Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerController) || !IsValid(PlayerActor))
	{
		CS3_Log(TEXT("UBaseMoveOperation::IsCanExecuteOperation : !IsValid(PlayerController) || !IsValid(PlayerActor)  return false!"));
		return false;
	}
	if (!PlayerController->CanMoveControl())
	{
		CS3_Log(TEXT("UBaseMoveOperation::IsCanExecuteOperation : !PlayerController->CanMoveControl()  return false!"));
		return false;
	}
	if (!IsValid(OperationModeMgr))
	{
		CS3_Log(TEXT("UBaseMoveOperation::IsCanExecuteOperation : !IsValid(OperationModeMgr)  return false!"));
		return false;
	}
	if (!OperationModeMgr->bIsAutoMove && (PlayerController->WasAltJustPressedOrReleased() ||
		PlayerController->WasCmdJustPressedOrReleased() ||
		PlayerController->WasCtrlJustPressedOrReleased() ||
		PlayerController->WasShiftJustPressedOrReleased())
		)
	{
		return false;
	}

	if (PlayerActor->IsDodgeState)
	{
		CS3_Log(TEXT("UBaseMoveOperation::IsCanExecuteOperation : PlayerActor->IsDodgeState  return false!"));
		return false;
	}
	return true;
}
#pragma endregion

#pragma region	前后方向移动操作(X)

bool UMoveForwardOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMoveForwardOperation::GetMoveVector : PlayerController || OperationModeMgr!"));
		return false;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetControlRotation();

	//获取相对玩家的前方向
	MoveVector = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家前
	MoveFlyVector = MoveVector;
	//获取被记录的向量
	KeepVector = OperationModeMgr->ForwardVector;

	return true;
}

#pragma endregion

#pragma region	左右方向移动操作(X)

bool UMoveRightOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UMoveRightOperation::GetMoveVector : PlayerController || OperationModeMgr!"));
		return false;
	}

	//判断是否为自动移动
	if (OperationModeMgr->bIsAutoMove)
	{
		//自动移动时，右方向的变量为0
		return false;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetControlRotation();

	//获取相对玩家的右方向
	MoveVector = UKismetMathLibrary::GetRightVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家右
	MoveFlyVector = MoveVector;
	//获取被记录的向量
	KeepVector = OperationModeMgr->RightVector;

	return true;
}

#pragma endregion

#pragma region	前后方向移动操作(Y)
bool UActionMoveForwardOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActionMoveForwardOperation::GetMoveVector : PlayerController || OperationModeMgr!"));
		return false;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetControlRotation();

	//获取相对玩家的前方向
	MoveVector = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家前
	MoveFlyVector = UKismetMathLibrary::GetForwardVector(FRotator(ControlRotator.Pitch, ControlRotator.Yaw, 0.0f));
	//获取被记录的向量
	KeepVector = OperationModeMgr->ForwardVector;

	return true;
}
#pragma endregion

#pragma region	左右方向移动操作(Y)
bool UActionMoveRightOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActionMoveRightOperation::GetMoveVector : PlayerController || OperationModeMgr!"));
		return false;
	}

	//判断是否为自动移动
	if (OperationModeMgr->bIsAutoMove)
	{
		//自动移动时，右方向的变量为0
		return false;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetControlRotation();

	//获取相对玩家的右方向
	MoveVector = UKismetMathLibrary::GetRightVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家右
	MoveFlyVector = UKismetMathLibrary::GetRightVector(FRotator(ControlRotator.Pitch, ControlRotator.Yaw, 0.0f));
	//获取被记录的向量
	KeepVector = OperationModeMgr->RightVector;

	return true;
}
#pragma endregion

#pragma region	载具前后移动
bool UVehicleMoveForwardOperation::GetMoveVector(FVector& MoveVector, FVector& MoveFlyVector, FVector& KeepVector)
{
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UVehicleMoveForwardOperation::GetMoveVector : PlayerController || OperationModeMgr!"));
		return false;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetActorRotation();

	//获取相对玩家的前方向
	MoveVector = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家前
	MoveFlyVector = MoveVector;
	//获取被记录的向量
	KeepVector = OperationModeMgr->ForwardVector;

	return true;
}
#pragma endregion

#pragma region	飞行上升移动操作
void UFlyUpOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UFlyUpOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerActor) || !IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::Tick : PlayerActor || PlayerController!"));
		return;
	}

	//是否是飞行状态
	if (PlayerController->IsFlying())
	{
		//获取玩家控制转向
		FRotator ControlRotator = PlayerActor->GetControlRotation();
		//获取玩家向上方向的向量
		FVector MoveUpByPlayer = UKismetMathLibrary::GetUpVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));

		//添加移动数据到数组
		PlayerController->AddMovementArray(MoveUpByPlayer, InputScale);
	}
}
#pragma endregion

#pragma region	匀速上升操作
void UYunSuUpOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	//Super::ExecuteOperation(InputKey, 1.0, OtherValue);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerController) || !IsValid(OperationModeMgr) || !IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseMoveOperation::ExecuteOperation : PlayerController || OperationModeMgr!"));
		return;
	}

	AActor *CurTarget = PlayerController->GetViewTarget();
	FVector CharacterDirection = PlayerActor->GetActorForwardVector();
	FVector ToLocation = CurTarget->GetActorLocation();
	//摄像机视角跟随玩家Z轴移动
	if (!PlayerActor->FeiShengProcressTargetActor)
	{
		UClass* GameCharacterClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("GameCharacter"));
		PlayerActor->FeiShengProcressTargetActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(GameCharacterClass);
		//PlayerActor->FeiShengProcressTargetActor->SetActorLabel("NewTargetActorFeiShengMoveUp");
		PlayerActor->FeiShengProcressTargetActor->SetActorEnableCollision(false);
		ToLocation = ToLocation + CharacterDirection * -(PlayerActor->FeiShengCameraLength);//向后移5米
	}	

	//左右移动
	if (InputScale != 0.0f)
	{
		int32 SizeX;
		int32 SizeY;
		PlayerController->GetViewportSize(SizeX, SizeY);
		FVector2D PlayerScreenPoint;
		PlayerController->ProjectWorldLocationToScreen(
			PlayerActor->GetActorLocation(), PlayerScreenPoint, true);
		/*CS3_Display(CS3DebugType::CL_Undefined, TEXT("Size(%d,  %d),  Screen(%f, %f),  (%f,   %f,  %f)"),
			SizeX, SizeY, PlayerScreenPoint.X, PlayerScreenPoint.Y,
			BeforLocation.X, BeforLocation.Y, BeforLocation.Z);*/
		if (PlayerScreenPoint.X < 0.0f || PlayerScreenPoint.X > SizeX)
		{
			PlayerActor->SetActorLocation(BeforLocation);
		}
		else
		{
			BeforLocation = PlayerActor->GetActorLocation();
			FRotator YawRotation(0, PlayerActor->GetControlRotation().Yaw, 0);
			FVector Direction = UKismetMathLibrary::GetRightVector(YawRotation);
			PlayerActor->AddMovementInput(Direction, InputScale);
		}
	}

	//上升
	float DeltaSeconds = UUECS3GameInstance::Instance->GetWorld()->GetDeltaSeconds();
	float MoveUpX = PlayerActor->GetActorLocation().X;// +DeltaSeconds * 1200 * InputScale;
	float MoveUpY = PlayerActor->GetActorLocation().Y;// +DeltaSeconds * 1200 * InputScale;
	float MoveUpZ = PlayerActor->GetActorLocation().Z + DeltaSeconds * PlayerActor->FeiShengUpSpeed;
	FVector MoveLocation = FVector(MoveUpX, MoveUpY, MoveUpZ);
	PlayerActor->SetActorLocation(MoveLocation);
	
	ToLocation.Z = MoveUpZ;
	PlayerActor->FeiShengProcressTargetActor->SetActorLocation(ToLocation);
	PlayerActor->FeiShengProcressTargetActor->SetActorRotation(PlayerActor->GetActorRotation());
	PlayerController->SetViewTargetWithBlend(PlayerActor->FeiShengProcressTargetActor, 0.0f,
		EViewTargetBlendFunction::VTBlend_Linear, 0.0f, true);
}	
	
#pragma endregion

#pragma region	固定移动朝向操作
void UKeepDirectionOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UKeepDirectionOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UKeepDirectionOperation::ExecuteOperation : OperationModeMgr!"));
		return;
	}

	//设置保持方向移动的相关属性
	OperationModeMgr->bIsKeepDirection = true;
}
#pragma endregion

#pragma region	取消固定移动朝向操作
void UUnKeepDirectionOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUnKeepDirectionOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UKeepDirectionOperation::ExecuteOperation : OperationModeMgr!"));
		return;
	}

	OperationModeMgr->bIsKeepDirection = false;
}
#pragma endregion

#pragma region	记录当前玩家前和右操作
void URecordPlayerVectorOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_URecordPlayerVectorOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(PlayerActor) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URecordPlayerVectorOperation::ExecuteOperation : PlayerActor || OperationModeMgr!"));
		return;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetControlRotation();
	//获取相对玩家的前方向
	FVector ForwardByPlayer = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//获取相对玩家的右方向
	FVector RightByPlayer = UKismetMathLibrary::GetRightVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));

	//设置记录玩家方向的相关属性
	OperationModeMgr->ForwardVector = ForwardByPlayer;
	OperationModeMgr->RightVector = RightByPlayer;
}
#pragma endregion

#pragma region	显示鼠标操作
void UShowMouseOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UShowMouseOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//获取UI管理器
	UGUIManager* GUIManager = UGolbalBPFunctionLibrary::GUIManager();

	if (!IsValid(PlayerController) || !IsValid(GUIManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UShowMouseOperation::ExecuteOperation : PlayerController || GUIManager!"));
		return;
	}

	//显示鼠标
	PlayerController->bShowMouseCursor = true;
	//设置输入模式
	UWidgetBlueprintLibrary::SetInputMode_GameAndUIEx
	(PlayerController, GUIManager->RootUIWidget, EMouseLockMode::DoNotLock, true);
}

#pragma region	隐藏鼠标操作
void UHideMouseOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UHideMouseOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//获取UI管理器
	UGUIManager* GUIManager = UGolbalBPFunctionLibrary::GUIManager();

	if (!IsValid(PlayerController) || !IsValid(GUIManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::Tick : PlayerController || GUIManager!"));
		return;
	}
	GUIManager->OnHideMouse();///<通知界面隐藏鼠标操作
	//隐藏鼠标
	PlayerController->bShowMouseCursor = false;
	UWidgetBlueprintLibrary::SetInputMode_GameOnly(PlayerController);
}
#pragma endregion

#pragma region	摄像机旋转基类
void UBaseCameraTurn::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseCameraTurn_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	float Scale = InputScale;
	if (IsValid(PlayerController))
	{
		///<由于Axis轴一个Tick连续输入2次值是一样的，在Axis事件中前提条件判断会有问题，因此/2
		Scale = PlayerController->GetMouseMoveScale()* InputScale / 2;
	}
	RotateOperation(Scale);
	//CS3_Warning(TEXT("UBaseCameraTurn::ExecuteOperation   Scale=%f  ,InputScale=%f !"), Scale, InputScale);
}
#pragma endregion

#pragma region	摄像机左右旋转(Y)
void UCameraTurnYOperation::RotateOperation(float InputScale)
{
	//获取控制器当前控制目标
	APawn* TagetPawn = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetPawn();

	if (!IsValid(TagetPawn))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraTurnYOperation::RotateOperation : PlayerActor!"));
		return;
	}

	//左右旋转摄像机
	TagetPawn->AddControllerYawInput(InputScale);
}
#pragma endregion

#pragma region	摄像机上下旋转(Y)
void UCameraLookUpYOperation::RotateOperation(float InputScale)
{
	//获取玩家
	APawn* TagetPawn = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetPawn();

	if (!IsValid(TagetPawn))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraLookUpYOperation::RotateOperation : PlayerActor!"));
		return;
	}

	//左右旋转摄像机
	TagetPawn->AddControllerPitchInput(InputScale);
}
#pragma endregion

#pragma region	练兵模式摄像机上下旋转(偏移最小值有做限制)
void UCameraLookUpTrainSoldierOperation::RotateOperation(float InputScale)
{
	//获取玩家
	APlayerController* Controller = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(Controller)) return;
	APawn* TagetPawn = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetPawn();

	if (!IsValid(TagetPawn))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraLookUpYOperation::RotateOperation : PlayerActor!"));
		return;
	}

	//上下旋转摄像机
	APlayerCameraManager* PlayerCameraManager = Controller->PlayerCameraManager;
	if (IsValid(PlayerCameraManager))
	{
		PlayerCameraManager->ViewPitchMax = -10.0f;
	}
	TagetPawn->AddControllerPitchInput(InputScale);

// 	FRotator RotationInput = Controller->RotationInput;
// 	RotationInput.Pitch += !Controller->IsLookInputIgnored() ? InputScale * Controller->InputPitchScale : 0.f;
// 	FRotator DeltaRot(RotationInput);
// 	FRotator ViewRotation = Controller->GetControlRotation() + DeltaRot;
// 	LimitViewPitch(ViewRotation, -89.9f, 10.0f);
// 
// 	Controller->SetControlRotation(ViewRotation);
// 	TagetPawn->FaceRotation(ViewRotation, UGolbalBPFunctionLibrary::GetDeltaTime());
}

void UCameraLookUpTrainSoldierOperation::LimitViewPitch(FRotator & OutViewRotation, float InViewPitchMin, float InViewPitchMax)
{
	OutViewRotation.Pitch = FMath::ClampAngle(OutViewRotation.Pitch, InViewPitchMin, InViewPitchMax);
	OutViewRotation.Pitch = FRotator::ClampAxis(OutViewRotation.Pitch);
}

#pragma endregion

#pragma region	摄像机左右旋转(X)
bool UCameraTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraTurnOperation::IsCanExecuteOperation : PlayerController!"));
		return false;
	}

	
	bool IsMouseXDown = PlayerController->IsInputKeyDown(EKeys::LeftMouseButton) &&
		PlayerController->CheckBindAxisActive(FName(TEXT("MouseLeftTurn")));
	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton) &&
		PlayerController->CheckBindAxisActive(FName(TEXT("MouseRightTurn")));

	if (!IsMouseXDown && !IsMouseYDown)
	{
		return false;
	}

	return true;
}

#pragma endregion

#pragma region	摄像机上下旋转(X)
bool UCameraLookUpOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraLookUpOperation::IsCanExecuteOperation : PlayerController!"));
		return false;
	}

	bool IsMouseXDown = PlayerController->IsInputKeyDown(EKeys::LeftMouseButton);
	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);

	if (!IsMouseXDown && !IsMouseYDown)
	{
		return false;
	}

	return true;
}

#pragma endregion

#pragma region	清除施法辅助操作
void UClearSkillAssisOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UClearSkillAssisOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//技能接口
	USkillInterface* PlayerSkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

	if (!IsValid(PlayerSkillInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UClearSkillAssisOperation::ExecuteOperation : PlayerSkillInterface!"));
		return;
	}

	//清除施法辅助操作
	PlayerSkillInterface->CancelSkillAssistUi();
}
#pragma endregion

#pragma region	点击地面移动操作
void UMoveByClickOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UMoveByClickOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{		
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (PlayerController->IsFlying())
	{
		PlayerController->MoveControlComponent->MouseClickFly();
	}
	else
	{
		PlayerController->MoveControlComponent->MouseClickMove();
	}
	PlayerController->bIsMouseClickNavMove = true;
}

bool UMoveByClickOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	//被服务器禁用了||不能移动则禁用||玩家在位置施法
	if (!IsValid(PlayerController) || !IsValid(OperationModeMgr) || !IsValid(PlayerActor)||
		(PlayerController->ControlMode == CONTROL_MODE::CONTROL_MODE_ACTION)||(!PlayerController->CanMoveControl())||(PlayerActor->GetSkillAssistUi()))
	{
		///<提示不能移动(摄像机没被操作了禁用此操作即没有左键旋转摄像机)
		if (IsValid(UUECS3GameInstance::Instance->MessageManager) && IsValid(UUECS3GameInstance::Instance->MessageManager)&&!OperationModeMgr->bIsCameraBeOperationed)
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(28);
		}
		CS3_Warning(TEXT("-->Null Pointer error:UMoveByClickOperation::IsCanExecuteOperation : PlayerController || OperationModeMgr || PlayerActor!"));
		return false;
	}
	
	//摄像机被操作了禁用此操作
	if (OperationModeMgr->bIsCameraBeOperationed)
	{
		return false;
	}
	return true;
}

#pragma endregion

#pragma region	通知玩家左击事件操作
void UCallLeftClickEventOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UCallLeftClickEventOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCallLeftClickEventOperation::ExecuteOperation : PlayerActor!"));
		return;
	}

	if (PlayerActor->GetSkillAssistUi())
	{
		PlayerActor->OnMouseLeftButtonClick();
	}
}
#pragma endregion

#pragma region	通知玩家右击事件操作
void UCallRightClickEventOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}
	//暂时没有功能预留
}
#pragma endregion

#pragma region	通知玩家Esc按键事件操作
void UCallEscClickEventOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->OnEscPressed();
	}
}
#pragma endregion

#pragma region	摄像机被操作操作
void UCameraBeOperationOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UCameraBeOperationOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraBeOperationOperation::ExecuteOperation : OperationModeMgr!"));
		return ;
	}
	if (InputScale != 0.0f)
	{
		OperationModeMgr->bIsCameraBeOperationed = true;
	}
}

bool UCameraBeOperationOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCameraBeOperationOperation::IsCanExecuteOperation : OperationModeMgr!"));
		return false;
	}
	if (!OperationModeMgr->bIsCameraBeOperationed)
	{
		//获取玩家控制器
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		//操作模式管理器
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

		if (IsValid(PlayerController)&&IsValid(ControllerModeMgr))
		{
			if (ControllerModeMgr->IsHaveMode(ECONTROL_MODE::DefaultControlMode))
			{
				bool IsMouseXDown = PlayerController->IsInputKeyDown(EKeys::LeftMouseButton);
				bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);
				if (IsMouseXDown || IsMouseYDown)
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
	}
	return false;
}
#pragma endregion

#pragma region	取消摄像机被操作操作
void UUnCameraBeOperationOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUnCameraBeOperationOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUnCameraBeOperationOperation::ExecuteOperation : OperationModeMgr!"));
		return;
	}

	OperationModeMgr->bIsCameraBeOperationed = false;
}
#pragma endregion

#pragma region	玩家旋转基类操作
bool UBaseTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	URoleStateInterface* RoleStateInst = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr);

	if (RoleStateInst && RoleStateInst->IsActionForbid(ACTION_FLAG::ACTION_FORBID_TRANSLATE_DIRECTION))
	{
		return false;
	}
	return true;
}
#pragma endregion

#pragma region	玩家旋转(类似ACT旋转，但是当IsCanExecuteOperation=false时玩家可以旋转，如鼠标点击地面玩家可以转向移动目标)
void USACTBaseTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_USACTBaseTurnOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::Tick : PlayerController || PlayerController!"));
		return;
	}

	if (!IsCanExecuteOperation())
	{
		//设置到玩家数据里
		PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 100000.0f;
		PlayerActor->bUseControllerRotationYaw = false;
		PlayerActor->CurMoveDirection = 0.0f;
		return;
	}

	//获取当前移动方向
	FVector MoveVector = PlayerActor->GetVelocity();

	//获取玩家的旋转
	float PlayerCurRotate = PlayerActor->GetActorRotation().Yaw;
	//获取玩家移动方向旋转值
	float PlayerMoverRotate = MoveVector.Rotation().Yaw;
	//计算旋转值的差
	float Tem = UKismetMathLibrary::FFloor((PlayerMoverRotate - PlayerCurRotate + 180.0f) / 360.0f) * 360.0f;
	float RotateVaule = PlayerMoverRotate - PlayerCurRotate - Tem;

	//设置到玩家数据里
	PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
	PlayerActor->bUseControllerRotationYaw = true;
	PlayerActor->CurMoveDirection = RotateVaule;
}
#pragma endregion

#pragma region	玩家旋转操作
void UTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UTurnOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTurnOperation::ExecuteOperation : PlayerActor!"));
		return;
	}

	if (!IsCanExecuteOperation())
	{
		PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
		PlayerActor->bUseControllerRotationYaw = false;
		PlayerActor->CurMoveDirection = 0.0f;
		return;
	}

	//设置到玩家数据里
	PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 100000.0f;
	PlayerActor->bUseControllerRotationYaw = false;
	PlayerActor->CurMoveDirection = 0.0f;
}

bool UTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	return true;
}

#pragma endregion

#pragma region	玩家Action旋转操作
void UActionTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UActionTurnOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::Tick : PlayerController || PlayerController!"));
		return;
	}

	if (!IsCanExecuteOperation())
	{
		//设置到玩家数据里
		PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
		PlayerActor->bUseControllerRotationYaw = false;
		PlayerActor->CurMoveDirection = 0.0f;
		return;
	}

	//获取当前移动方向
	FVector MoveVector = PlayerActor->GetVelocity();

	//获取玩家的旋转
	float PlayerCurRotate = PlayerActor->GetActorRotation().Yaw;
	//获取玩家移动方向旋转值
	float PlayerMoverRotate = MoveVector.Rotation().Yaw;
	//计算旋转值的差
	float Tem = UKismetMathLibrary::FFloor((PlayerMoverRotate - PlayerCurRotate + 180.0f) / 360.0f) * 360.0f;
	float RotateVaule = PlayerMoverRotate - PlayerCurRotate - Tem;

	//设置到玩家数据里
	PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
	PlayerActor->bUseControllerRotationYaw = true;
	PlayerActor->CurMoveDirection = RotateVaule;
}

bool UActionTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	return true;
}

#pragma endregion


#pragma region	玩家ALT旋转操作
void UALTTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UALTTurnOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UALTTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UALTTurnOperation::IsCanExecuteOperation : PlayerController!"));
		return false;
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UALTTurnOperation::ExecuteOperation : OperationModeMgr!"));
		return false;
	}
	float DeltaX, DeltaY = 0.0f;
	PlayerController->GetInputMouseDelta(DeltaX, DeltaY);
	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);

	if (IsMouseYDown && DeltaX != 0 && OperationModeMgr->bIsCanTurn == true)
	{
		return true;
	}

	return false;
}

void UFlyTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UFlyTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyTurnOperation::IsCanExecuteOperation : PlayerController!"));
		return false;
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFlyTurnOperation::IsCanExecuteOperation : OperationModeMgr!"));
		return false;
	}
	float DeltaX, DeltaY = 0.0f;
	PlayerController->GetInputMouseDelta(DeltaX, DeltaY);
	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);

	if (IsMouseYDown && DeltaX != 0 && OperationModeMgr->bIsCanTurn == true)
	{
		return true;
	}

	return false;
}

bool UGlidingTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGlidingTurnOperation::IsCanExecuteOperation : PlayerController!"));
		return false;
	}
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGlidingTurnOperation::IsCanExecuteOperation: OperationModeMgr!"));
		return false;
	}	
	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);

	if (IsMouseYDown || OperationModeMgr->bIsCanTurn == true)
	{
		return true;
	}
	return false;
}

bool UFallTurnOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	return true;
}
#pragma endregion

#pragma region	玩家是否能旋转
void UActorCanTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UActorCanTurnOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActorCanTurnOperation::ExecuteOperation: OperationModeMgr!"));
		return;
	}
	if ((InputScale != 0.0f) || (OldInputScale != 0.0f && InputScale == 0.0f))
	{		
		OperationModeMgr->bIsCanTurn = true;
	}
	else
	{
		OperationModeMgr->bIsCanTurn = false;
	}
	OldInputScale = InputScale;
}
#pragma endregion

#pragma region 开启自动移动
void UOpenAutoMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UOpenAutoMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UOpenAutoMoveOperation::ExecuteOperation: OperationModeMgr!"));
			return;
	}

	OperationModeMgr->bIsAutoMove = true;
}
#pragma endregion

#pragma region 关闭自动移动
void UCloseAutoMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UCloseAutoMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();

	if (!IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCloseAutoMoveOperation::ExecuteOperation: OperationModeMgr!"));
			return;
	}

	OperationModeMgr->bIsAutoMove = false;
}
#pragma endregion

#pragma region 闪避基类
void UBaseDodgeOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseDodgeOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}
	DeferredUseSkill();
}

bool UBaseDodgeOperation::IsCanExecuteOperation()
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseDodgeOperation_ExecuteOperation);
	Super::IsCanExecuteOperation();

	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	/*APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor)&& PlayerActor->IsDodgeState)
	{
		return false;
	}*/
	return true;
}

FRotator UBaseDodgeOperation::GetRoleNewRotation()
{
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		FRotator MyRotation = PlayerActor->GetActorRotation();
		MyRotation.Yaw = PlayerActor->GetControlRotation().Yaw;
		//思路：根据角色控制器视角角度为基础，来进行前后左右计算偏移角度
		return MyRotation;
	}
	return FRotator();
}

bool UBaseDodgeOperation::GetRoleStartRotation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		FRotator NewRotation = GetRoleNewRotation();
		PlayerActor->DodgeRotator = NewRotation;
		//PlayerActor->SetActorRotation(GetRoleNewRotation());
		return true;				
	}
	return false;
}

void UBaseDodgeOperation::DeferredUseSkill()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(PlayerActor) && IsValid(PlayerController) && IsValid(ControllerModeMgr))
	{
		USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
		if (IsValid(SkillInterface))
		{
			URoleStateInterface* RoleStateInst = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr);
			bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);
			bool IsActModel = ControllerModeMgr->IsHaveMode(ECONTROL_MODE::ActionControlMode);
			bool bIsYCJMDCopy = PlayerActor->bIsYCJMDCopy;///远程吃鸡里要求闪避能按方向转向

			int32 SkillId = 0;
			if (IsMouseYDown || IsActModel || bIsYCJMDCopy)
			{
				SkillId = GetDodgeSkillID();
			}
			else
			{
				SkillId = GetFrontDodgeSkillID();
			}
			//bool IsPassConditional = SkillInterface->CheckSkillUseCondition(SkillId);
			//if (IsPassConditional)
			{
				if (!IsMouseYDown && !IsActModel)
				{
					GetRoleStartRotation();
				}
				else
				{					
					FRotator MyRotation = PlayerActor->GetActorRotation();
					MyRotation.Yaw = PlayerActor->GetControlRotation().Yaw;
					//PlayerActor->SetActorRotation(MyRotation);
					PlayerActor->DodgeRotator = MyRotation;
				}
				SkillInterface->UseSkill(SkillId, PlayerActor->EntityId);				
			}
		}
		else
		{
			CS3_Warning(TEXT("UBaseDodgeOperation::ExecuteOperation --- SkillInterface Is Null !"));
		}
	}
	else
	{
		CS3_Warning(TEXT("UBaseDodgeOperation::ExecuteOperation --- PlayerActor Is Null !"));
	}
}
#pragma endregion

#pragma region 前闪避
FRotator  UDodgeFrontOperation::GetRoleNewRotation()
{
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	
	if (IsValid(PlayerActor))
	{
		FRotator MyRotation = PlayerActor->GetActorRotation();
		MyRotation.Yaw = PlayerActor->GetControlRotation().Yaw;

		return MyRotation;
	}
	return FRotator();
}
#pragma endregion

#pragma region 后闪避
FRotator  UDodgeBackOperation::GetRoleNewRotation()
{
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		FRotator MyRotation = PlayerActor->GetActorRotation();
		float ControlYaw = PlayerActor->GetControlRotation().Yaw;
		int32 Value = ControlYaw >= 0.0f ? 1 : -1;
		MyRotation.Yaw = ControlYaw - 180.0f * Value;

		return MyRotation;
	}
	return FRotator();
}

#pragma endregion

#pragma region 左闪避
FRotator  UDodgeLeftOperation::GetRoleNewRotation()
{
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	FRotator MyRotation = PlayerActor->GetActorRotation();
	float ControlYaw = PlayerActor->GetControlRotation().Yaw;
	if (IsValid(PlayerActor))
	{
		if (ControlYaw > 0)
		{
			MyRotation.Yaw = ControlYaw - 90.0f;
		}
		else
		{
			MyRotation.Yaw = ControlYaw + 180.0f + 90;
		}

		return MyRotation;
	}
	return FRotator();
}

#pragma endregion

#pragma region 右闪避
FRotator  UDodgeRightOperation::GetRoleNewRotation()
{
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	FRotator MyRotation = PlayerActor->GetActorRotation();
	float ControlYaw = PlayerActor->GetControlRotation().Yaw;

	if (ControlYaw > 0)
	{
		MyRotation.Yaw = ControlYaw - 180.0 - 90.0f;
	}
	else
	{
		MyRotation.Yaw = ControlYaw + 90.0f;
	}
	return MyRotation;
}


#pragma endregion

#pragma region 镜头缩放基类
void UBaseFlexHandleOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseFlexHandleOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseFlexHandleOperation::ExecuteOperation: PlayerActor!"));
		return;
	}
	if (PlayerActor->IsSkillAssistTurn())
	{
		return;
	}

	if (!UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->isArmLimit)
	{
		//获取臂杆长度
		auto SpringCon = PlayerActor->SpringArmCompent;
		if (SpringCon != nullptr)
		{

			const float MaxFOV = 90;
			float MinFOV = 30;
			float FOVChangeSpeed = 0.2;
			float ChangeSpeed = 0.5;

			float CameraArmLenMax;
			float CameraArmLenMin;
			const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
			GameInstance->LocalDataSaveManager->LocalUserSettingData->GetCameraArmLenData(CameraArmLenMax, CameraArmLenMin);

			auto Camera = PlayerActor->CameraComponent;
			auto OldFOV = Camera->FieldOfView;
			float FOVMaxLength = (MaxFOV - MinFOV) / FOVChangeSpeed;
			float SimulateLength = (OldFOV - MinFOV) / FOVChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, FOVMaxLength);
			float ArmLength = SpringCon->TargetArmLength;
			ArmLength = ArmLength - CameraArmLenMin;
			ArmLength = FMath::Max(ArmLength, 0.0f);
			SimulateLength += ArmLength;
			float Speed = GetSpeed();
			SimulateLength += Speed * ChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, (CameraArmLenMax - CameraArmLenMin) + FOVMaxLength);
			if (SimulateLength > FOVMaxLength)
			{
				Camera->FieldOfView = MaxFOV;
				SpringCon->TargetArmLength = SimulateLength - FOVMaxLength + CameraArmLenMin;
			}
			else {
				Camera->FieldOfView = SimulateLength * FOVChangeSpeed + MinFOV;
				SpringCon->TargetArmLength = CameraArmLenMin;
			}



			if (SimulateLength <= CameraArmLenMin+70)
			{
				PlayerActor->isOpenLookCamera = true;
			}
			else
			{
				PlayerActor->isOpenLookCamera = false;
			}
		}else
		{
			///切换了控制只有 非玩家Actor 旋转设置
			AMovingPlatformShipsCharacter* XianzhouTarget = Cast<AMovingPlatformShipsCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetPawn());
			if (IsValid(XianzhouTarget))
			{
				auto TargetSpringCon = XianzhouTarget->SpringArmCompent;
				float ArmLength = TargetSpringCon->TargetArmLength;
				ArmLength += GetSpeed();
				UGolbalBPFunctionLibrary::SetCameraTargetArmLength(XianzhouTarget->SpringArmCompent, ArmLength);
			}
		}
	}
}
#pragma endregion

#pragma region 模型旋转基类
void UBaseFlexHandleOperation_ModelTurn::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaseFlexHandleOperation_ModelTurn_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseFlexHandleOperation_ModelTurn::ExecuteOperation: PlayerActor!"));
		return;
	}
	if (PlayerActor->IsSkillAssistTurn())
	{
		PlayerActor->OnMouseScrollRoll(GetSpeed());
	}

}
#pragma endregion

#pragma region 怪物镜头缩放基类
void UBaseFlexHandleOperation_Monster::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器控制的Pawn
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor)) return;
	AMonsterGhostEyeCharacter* MonsterGhostEye = Cast<AMonsterGhostEyeCharacter>(ControlActor);
	if (!IsValid(MonsterGhostEye)) return;

	if (!UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->isArmLimit)
	{
		//获取臂杆长度
		auto SpringCon = MonsterGhostEye->SpringArmCompent;
		if (SpringCon != nullptr)
		{
			const float MaxFOV = 90;
			float MinFOV = 30;
			float FOVChangeSpeed = 0.2;
			float ChangeSpeed = 0.5;

			float CameraArmLenMax;
			float CameraArmLenMin;
			const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
			if (!IsValid(GameInstance)) return;
			if (!IsValid(GameInstance->LocalDataSaveManager)) return;
			ULocalUserSettingData* LocalUserSettingData = GameInstance->LocalDataSaveManager->LocalUserSettingData;
			if (!IsValid(LocalUserSettingData)) return;
			LocalUserSettingData->GetCameraArmLenData(CameraArmLenMax, CameraArmLenMin);

			auto Camera = MonsterGhostEye->CameraComponent;
			auto OldFOV = Camera->FieldOfView;
			float FOVMaxLength = (MaxFOV - MinFOV) / FOVChangeSpeed;
			float SimulateLength = (OldFOV - MinFOV) / FOVChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, FOVMaxLength);
			float ArmLength = SpringCon->TargetArmLength;
			ArmLength = ArmLength - CameraArmLenMin;
			ArmLength = FMath::Max(ArmLength, 0.0f);
			SimulateLength += ArmLength;
			float Speed = GetSpeed();
			SimulateLength += Speed * ChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, (CameraArmLenMax - CameraArmLenMin) + FOVMaxLength);
			if (SimulateLength > FOVMaxLength)
			{
				Camera->FieldOfView = MaxFOV;
				SpringCon->TargetArmLength = SimulateLength - FOVMaxLength + CameraArmLenMin;
			}
			else 
			{
				Camera->FieldOfView = SimulateLength * FOVChangeSpeed + MinFOV;
				SpringCon->TargetArmLength = CameraArmLenMin;
			}
		}
	}
}
#pragma endregion

#pragma region 坐骑镜头缩放基类
void UBaseFlexHandleOperation_Vehicle::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器控制的Pawn
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor)) return;
	AMovingPlatformVehicleCharacter* MovingPlatformVehicleCharacter = Cast<AMovingPlatformVehicleCharacter>(ControlActor);
	if (!IsValid(MovingPlatformVehicleCharacter)) return;

	if (!UGolbalBPFunctionLibrary::GetCS3PlayerController()->CS3ConSoleMgr->isArmLimit)
	{
		//获取臂杆长度
		auto SpringCon = MovingPlatformVehicleCharacter->SpringArmCompent;
		if (SpringCon != nullptr)
		{
			const float MaxFOV = 90;
			float MinFOV = 30;
			float FOVChangeSpeed = 0.2;
			float ChangeSpeed = 0.5;

			float CameraArmLenMax;
			float CameraArmLenMin;
			const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
			if (!IsValid(GameInstance)) return;
			if (!IsValid(GameInstance->LocalDataSaveManager)) return;
			ULocalUserSettingData* LocalUserSettingData = GameInstance->LocalDataSaveManager->LocalUserSettingData;
			if (!IsValid(LocalUserSettingData)) return;
			LocalUserSettingData->GetCameraArmLenData(CameraArmLenMax, CameraArmLenMin);

			auto Camera = MovingPlatformVehicleCharacter->CameraComponent;
			auto OldFOV = Camera->FieldOfView;
			float FOVMaxLength = (MaxFOV - MinFOV) / FOVChangeSpeed;
			float SimulateLength = (OldFOV - MinFOV) / FOVChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, FOVMaxLength);
			float ArmLength = SpringCon->TargetArmLength;
			ArmLength = ArmLength - CameraArmLenMin;
			ArmLength = FMath::Max(ArmLength, 0.0f);
			SimulateLength += ArmLength;
			float Speed = GetSpeed();
			SimulateLength += Speed * ChangeSpeed;
			SimulateLength = FMath::Clamp(SimulateLength, 0.0f, (CameraArmLenMax - CameraArmLenMin) + FOVMaxLength);
			if (SimulateLength > FOVMaxLength)
			{
				Camera->FieldOfView = MaxFOV;
				SpringCon->TargetArmLength = SimulateLength - FOVMaxLength + CameraArmLenMin;
			}
			else
			{
				Camera->FieldOfView = SimulateLength * FOVChangeSpeed + MinFOV;
				SpringCon->TargetArmLength = CameraArmLenMin;
			}
		}
	}
}
#pragma endregion

#pragma region 切换到Alt模式
void USwitchToAltOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_USwitchToAltOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
		return;

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(ControllerModeMgr) || !IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USwitchToAltOperation::ExecuteOperation : ControllerModeMgr!"));
		return;
	}

	if (ControllerModeMgr->IsHaveMode(ECONTROL_MODE::AltControlMode))
	{
		///<在非X模式下，按ALt组合键的操作不执行ALT模式切换
		if (PlayerController->CheckKeyExecutedByActionKey(EKeys::LeftAlt))
			return;
		//恢复到背景模式
		ControllerModeMgr->RecoveryMode();
	}
	else if (!ControllerModeMgr->IsHaveMode(ECONTROL_MODE::DefaultControlMode))
	{
		///<在非X模式下，按ALt组合键的操作不执行ALT模式切换
		if (PlayerController->CheckKeyExecutedByActionKey(EKeys::LeftAlt))
			return;

		//切换到Alt模式
		ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::AltControlMode, CC_MODE_REASON::CCM_ALT_CONTOLLER_MODE);
	}
}

bool USwitchToAltOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	if (!UUECS3GameInstance::Instance->IsGameWindowActive())
	{
		return false;
	}

	return true;
}

#pragma endregion

#pragma region 重置已按下键操作
void UFlushPressedKeysOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UFlushPressedKeysOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		PlayerController->PlayerInput->FlushPressedKeys();
	}
}
#pragma endregion

#pragma region 切换到YControl模式
void USwitchToYControlOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_USwitchToYControlOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (!IsValid(ControllerModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USwitchToYControlOperation::ExecuteOperation: ControllerModeMgr!"));
		return;
	}

	ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::YControlMode, CC_MODE_REASON::CCM_Y_CONTROLLER_MODE);
}
#pragma endregion

#pragma region 恢复到背景模式
void URecoveryModeOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_URecoveryModeOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (!IsValid(ControllerModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URecoveryModeOperation::ExecuteOperation: ControllerModeMgr!"));
		return;
	}

	ControllerModeMgr->RecoveryMode();
}
#pragma endregion

#pragma region 跳跃操作
void UJumpPressedOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UJumpPressedOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor) && !IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UJumpPressedOperation::ExecuteOperation: PlayerActor || PlayerController!"));
		return;
	}

	if (IsValid(PlayerActor) && IsValid(PlayerActor->JumpComponent))
	{
		PlayerActor->JumpComponent->OnStartActiveJump();
	}
}
#pragma endregion

#pragma region 停止跳跃操作
void UJumpReleasedOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UJumpReleasedOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor) && !IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UJumpReleasedOperation::ExecuteOperation: PlayerActor || PlayerController!"));
		return;
	}

	if (PlayerActor->bPressedJump)
	{
		FTimerHandle DelayHandle;
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(DelayHandle, PlayerActor, &APlayerCharacter::StopJumping, 0.1f, false);
		}
	}
	else
	{
		PlayerActor->StopJumping();
	}
}
#pragma endregion

#pragma region 跳跃及停止操作（控制器控制的pawn）
void UPawnJumpPressedOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	//获取玩家控制器控制的Pawn
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor))
	{
		return;
	}
	ControlActor->Jump();
}

bool UPawnJumpPressedOperation::IsCanExecuteOperation()
{
	return true;
}

void UPawnJumpReleasedOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	//获取玩家控制器控制的Pawn
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor))
	{
		return;
	}
	ControlActor->StopJumping();
}

bool UPawnJumpReleasedOperation::IsCanExecuteOperation()
{
	return true;
}
#pragma endregion

#pragma region 切换快捷栏按键到Dafault
void USwitchToDafaultQuickOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_USwitchToDafaultQuickOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USwitchToDafaultQuickOperation::ExecuteOperation: PlayerController!"));
		return;
	}

	PlayerController->ChangeBindShortcutKeyByControlMode(ECONTROL_MODE::DefaultControlMode, ECONTROL_MODE::ActionControlMode);
}
#pragma endregion

#pragma region 切换快捷栏按键到Action
void USwitchToActionQuickOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_USwitchToActionQuickOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USwitchToActionQuickOperation::ExecuteOperation: PlayerController!"));
		return;
	}

	PlayerController->ChangeBindShortcutKeyByControlMode(ECONTROL_MODE::ActionControlMode, ECONTROL_MODE::DefaultControlMode);
}
#pragma endregion

#pragma region 设置玩家可以Actor旋转 当前用在自动寻路中 禁止玩家旋转Y轴随ControllerRotationYaw
void UActorCanRotateOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UActorCanRotateOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActorCanRotateOperation::ExecuteOperation: PlayerActor!"));
		return;
	}

	//设置到玩家数据里
	PlayerActor->GetCharacterMovement()->RotationRate.Yaw = 100000.0f;
	PlayerActor->bUseControllerRotationYaw = false;
	PlayerActor->CurMoveDirection = 0.0f;
}
#pragma endregion


#pragma region 调整摄像机视角
void UAdjustViewTargetWithBlendOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UAdjustViewTargetWithBlendOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAdjustViewTargetWithBlendOperation: PlayerActor!"));
		return;
	}
	PlayerActor->AtuoAdjustViewTargetWithBlend();
}
#pragma endregion

#pragma region 取消调整摄像机视角
void UUnAdjustViewTargetWithBlendOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUnAdjustViewTargetWithBlendOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor) )
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUnAdjustViewTargetWithBlendOperation::ExecuteOperation: PlayerActor!"));
		return;
	}
	PlayerActor->UnAdjustViewTargetWithBlend();
}
#pragma endregion


#pragma region 使用技能
void UUseSkillOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseSkillOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	USkillInterface* RoleSkillInst = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

	if (!IsCanExecuteOperation())
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(8);//您现在无法使用技能
		return;
	}

	//参数判断
	if (OtherValue.Num()< 2)
	{
		CS3_Warning(TEXT("UUseSkillOperation::ExecuteOperation --- OtherValue Is ERROR!"));
		return;
	}
	
	USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;

	if (!IsValid(SkillInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseSkillOperation::ExecuteOperation: SkillInterface!"));
		return;
	}

	SkillInterface->UseSkill(FSTRING_TO_INT(OtherValue[0]), FSTRING_TO_INT(OtherValue[1]));
}

bool UUseSkillOperation::IsCanExecuteOperation()
{
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		if (Interface->HasVehicle())
		{
			return false;
		}
	}
	return true;
}

#pragma endregion

#pragma region 使用物品
void UUseItemBaseOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseItemBaseOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取物品
	UItemUse* ItemUse = Cast<UItemUse>(GetItem(OtherValue));

	//判断参数
	if (!IsValid(ItemUse))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseItemBaseOperation::ExecuteOperation: ItemUse!"));
		return;
	}
	ItemUse->Use(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
}
#pragma endregion

#pragma region 在快捷栏使用物品
void UUseItemInQuickOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseItemInQuickOperation_ExecuteOperation);
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//参数判断
	if (OtherValue.Num() < 2)
	{
		CS3_Warning(TEXT("UUseItemInQuickOperation::ExecuteOperation --- OtherValue Is ERROR!"));
		return;
	}

	int32 ItemId = FSTRING_TO_INT(OtherValue[1]);
	AServerCharacter* UseCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (!IsValid(UseCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseItemInQuickOperation::ExecuteOperation: UseCharacter!"));
		return;
	}

	//获取玩家的背包
	URoleKitBagInterface* KitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));

	if (!IsValid(KitBagInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseItemInQuickOperation::ExecuteOperation: KitBagInterface!"));
		return;
	}

	//获取物品
	TArray<UItemBase*> ItemPtrs = KitBagInterface->GetItemsByItemID(ItemId);

	UItemBase* ItemPtr = nullptr;

	if (ItemPtrs.Num() > 0)
	{
		ItemPtr = ItemPtrs[0];
	}
	else
	{
		CS3_Warning(TEXT("UseItemInQuickOperation::ExecuteOperation Don't Find This Item!"));
		return;
	}

	UItemUse* ItemUsePtr = Cast<UItemUse>(ItemPtr);

	//判断能否使用物品
	if (IsValid(ItemUsePtr))
	{
		int32 CheckUseResult = ItemUsePtr->UseQuery(UseCharacter);
		//判断物品是否符合使用的条件
		if (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG == CheckUseResult)
		{
			if (!ItemUsePtr->IsUseItemToPosition())
			{
				int32 targetID = UGolbalBPFunctionLibrary::GetTargetEntityID();
				KitBagInterface->RPC_uesItemByShortcutBar(ItemUsePtr->ItemID, targetID);
			}
			return;
		}
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(CheckUseResult);
			return;
		}
	}
	else
	{
		return;
	}
}

bool UUseItemInQuickOperation::IsCanExecuteOperation()
{
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		if (Interface->HasVehicle())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(621);//在骑乘状态下，不能使用该物品
			return false;
		}
	}
	return true;
}

UItemBase* UUseItemInQuickOperation::GetItem(TArray<FString>& OtherValue)
{
	//参数判断
	if (OtherValue.Num() < 3)
	{
		CS3_Warning(TEXT("UUseItemInQuickOperation::ExecuteOperation --- OtherValue Is ERROR!"));
		return nullptr;
	}

	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>
		(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));

	bool BindType = UKismetMathLibrary::Conv_IntToBool(FSTRING_TO_INT(OtherValue[2]));

	TArray<UItemBase*> Items = RoleKitBagInterface->GetItemsByBindType
	(FSTRING_TO_INT(OtherValue[1]), BindType);

	if (Items.Num() <= 0)
	{
		CS3_Warning(TEXT("物品不存在，不能使用"));
		return nullptr;
	}

	return Items[0];
}
#pragma endregion

#pragma region 在背包使用物品

bool UUseItemInBagOperation::IsCanExecuteOperation()
{
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		if (Interface->HasVehicle())
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(621);//在骑乘状态下，不能使用该物品
			return false;
		}
	}
	return true;
}

UItemBase* UUseItemInBagOperation::GetItem(TArray<FString>& OtherValue)
{
	//参数判断
	if (OtherValue.Num() < 2)
	{
		CS3_Warning(TEXT("UUseItemInQuickOperation::ExecuteOperation --- OtherValue Is ERROR!"));
		return nullptr;
	}

	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>
		(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));

	UItemBase* ItemUse = RoleKitBagInterface->FindItemByUID(OtherValue[1]);

	return ItemUse;
}
#pragma endregion

#pragma region 检测是否进入Y操作
void UCheckChangeToYOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UCheckChangeToYOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCheckChangeToYOperation::ExecuteOperation: PlayerController!"));
		return;
	}

	if (PlayerController->IsInputKeyDown(EKeys::RightMouseButton))
	{
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

		if (IsValid(ControllerModeMgr))
		{
			ControllerModeMgr->ChangeControllerMode(ECONTROL_MODE::YControlMode, CC_MODE_REASON::CCM_Y_CONTROLLER_MODE);
		}
	}
}
#pragma endregion

#pragma region	荷花移动操作基类

void UHeHuaBaseMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UHeHuaBaseMoveOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));

	if (Interface)
	{
		return Interface->IsMovingCallCellOnHeHua();
	}
	return false;
}

void UHeHuaBaseMoveOperation::OnCallServerMethod(const FString& DirectionName)
{
	if (DirectionName.IsEmpty())
		return;

	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));

	if (IsValid(Interface))
	{
		Interface->bIsMovingToCallCellOnHeHua = true;
		Interface->RPC_move(DirectionName);
	}
}

#pragma endregion

#pragma region	荷花移动操作WSAD类
void UHeHuaForwardMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UHeHuaForwardMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (IsCanExecuteOperation())
	{
		OnCallServerMethod(TEXT("w"));
	}
}

void UHeHuaBackwardsMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UHeHuaBackwardsMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (IsCanExecuteOperation())
	{
		OnCallServerMethod(TEXT("s"));
	}
}

void UHeHuaRightsMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UHeHuaRightsMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (IsCanExecuteOperation())
	{
		OnCallServerMethod(TEXT("d"));
	}
}

void UHeHuaLeftMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UHeHuaLeftMoveOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (IsCanExecuteOperation())
	{
		OnCallServerMethod(TEXT("a"));
	}
}
#pragma endregion

#pragma region	下荷花操作
void UDismountHeHuaOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UDismountHeHuaOperation_ExecuteOperation);
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UDismountHeHuaOperation::ExecuteOperation: PlayerActor!"));
		return;
	}
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));

	if (Interface)
	{
		if (!Interface->bIsMovingOnHeHua)
		{
			Interface->OnDismountHeHua();
		}
	}
}

#pragma endregion

#pragma region	随机动作行为
void URandomActionOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_URandomActionOperation_ExecuteOperation);
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerActor) || !PlayerActor->GetSelfEntity()|| !IsValid(PlayerActor->GetMovementComponent()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URandomActionOperation::ExecuteOperation: PlayerActor) || PlayerActor->GetSelfEntity()|| PlayerActor->GetMovementComponent()!"));
		return;
	}

	if (!UUECS3GameInstance::Instance->GameStatus || !PlayerActor->GetBaseAnimInstance() ||
		PlayerActor->bIsRoleInteractive || UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() != EGameStatus::InWorld
		|| PlayerActor->GetMovementComponent()->IsFlying() || PlayerActor->GetMovementComponent()->IsSwimming())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("URandomActionOperation::ExecuteOperation --- RandomAction Play Fail !"));
		return;
	}

	bool IsAtStandBy = PlayerActor->GetBaseAnimInstance()->IsStandByState();
	StandTime++;
	StandTime = IsAtStandBy ? StandTime : 0;

	int32 RandomActionTimeMin = UUECS3GameInstance::Instance->GameDefault->RandomActionTimeMin;
	int32 RandomActionTimeMax = UUECS3GameInstance::Instance->GameDefault->RandomActionTimeMax;
	int32 RandomNum = FMath::RandRange(RandomActionTimeMin, RandomActionTimeMax);
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("======= name=%s,    time=%d,   RandomNum=%d, IsAtStandBy=%d"), *this->GetName(), StandTime, RandomNum, IsAtStandBy?1:0);
	if (StandTime >= RandomNum)
	{
		StandTime = 0;
		URoleInterface * RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.GameObjectInterface : nullptr);
		if (RoleInterface)
		{
			RoleInterface->RequestPlayRandomAction();
		}
		//KBEngine::FVariantArray Args;
		//PlayerActor->GetSelfEntity()->CellCall(TEXT("RequestPlayRandomAction"), Args);
	}
}
#pragma endregion

#pragma region UseSkillOfBaseShoot

FString UUseSkillOfBaseShoot::GetSkillIDByState(int32 Index)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseSkillOperation_GetSkillIDByState);
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
	{
		UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();

		if (AtkStateMar->IsActivateState(EATTACT_STATE::BEHAVIOR_SHOOT))
		{
			UAtkStateBase*  ShootAtkState = AtkStateMar->GetCurAtkState();

			if (IsValid(ShootAtkState))
			{
				UShootMode* ShootMode = Cast<UShootMode>(ShootAtkState);
				if (IsValid(ShootMode))
				{
					TArray<FString> OtherValue = ControllerModeMgr->GetOtherValue();
					FString StateName = ShootMode->GetStateType();
					int32 StateOtherValue = FSTRING_TO_INT(ShootMode->GetOtherValue());
					if (Index==1&&(!StateName.Compare("YCJMD")|| !StateName.Compare("HSBZ")))
					{
						return INT_TO_FSTRING(StateOtherValue);
					}
					for (FString data : OtherValue)
					{
						TArray<FString> StateData = UGolbalBPFunctionLibrary::SplitString(data);
						if (StateData.Num() > 0 && StateData.Num() > Index)
						{
							if (!StateData[0].Compare(StateName))
							{
								if (StateOtherValue > 0)
								{
									TArray<FString> StateOtherValueData = UGolbalBPFunctionLibrary::SplitString(StateData[Index], false, TEXT(";"));
									if (StateOtherValueData.Num() > 2 && StateOtherValueData.Num() >= (StateOtherValue - 1))
									{
										return StateOtherValueData[StateOtherValue - 1];
									}
								}
								return StateData[Index];
							}
						}
					}
				}
			}
		}
	}
	return TEXT("");
}
#pragma endregion

#pragma region 使用射击技能
void UUseSkillOfShoot::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseSkillOfShoot_ExecuteOperation);

	///<优先考虑位置施法（以当前准心的位置为基准）
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseSkillOfLineShoot::ExecuteOperation: PlayerController!"));
		return;
	}
	if (!IsValid(PlayerActor)) return;
	if (PlayerActor->GetSkillAssistUi())
	{
		int32 SizeX = 0, SizeY = 0;
		PlayerController->GetViewportSize(SizeX, SizeY);
		FHitResult TraceHitResult;
		FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true);
		TraceParams.bTraceComplex = true;
		TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		PlayerController->GetHitResultAtScreenPosition(FVector2D(SizeX / 2.0f, SizeY / 2.0f), PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
		if (TraceHitResult.bBlockingHit)
		{
			PlayerActor->OnSimulateMouseLeftButtonClick(TraceHitResult.ImpactPoint);
			return;
		}
		else
		{
			FVector WorldOrigin;
			FVector WorldDirection;
			if (UGameplayStatics::DeprojectScreenToWorld(PlayerController, FVector2D(SizeX / 2.0f, SizeY / 2.0f), WorldOrigin, WorldDirection) == true)
			{
				PlayerActor->OnSimulateMouseLeftButtonClick(WorldOrigin + WorldDirection * 5000.0f);
				return;
			}
		}

	}
	FString SkillID = GetSkillIDByState(1);
	if (SkillID.IsEmpty())return;
	OtherValue.Empty();
	OtherValue.Add(SkillID);
	OtherValue.Add(TEXT("0"));

	TWeakObjectPtr<UUseSkillOfShoot> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, AutoShootHandle, FTimerDelegate::CreateLambda([OtherValue, DelayThisPtr]()
	{
		if (DelayThisPtr.IsValid())
		{
			UUseSkillOfShoot* ThisPtr = DelayThisPtr.Get();
			ThisPtr->Super::ExecuteOperation(TEXT(""), 0.0f, OtherValue);
		}
	}
	), 0.5f, true);

	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	UGolbalBPFunctionLibrary::GEventManager()->OnCloseAutoShoot = FOnCloseAutoShoot::CreateLambda([this]()
	{
		CloseAutoShoot();
	});
	UsePositionSkill();
}

void UUseSkillOfShoot::CloseAutoShoot()
{
	if (AutoShootHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(AutoShootHandle);
	}
}
void UUseSkillOfShoot::UsePositionSkill()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerActor) && IsValid(PlayerController) && PlayerActor->GetSkillAssistUi())
	{
		UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
		UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
		if (AtkStateMar->IsActivateState(EATTACT_STATE::BEHAVIOR_SHOOT))
		{
			UAtkStateBase*  ShootAtkState = AtkStateMar->GetCurAtkState();

			if (IsValid(ShootAtkState))
			{
				UShootMode* ShootMode = Cast<UShootMode>(ShootAtkState);

				if (IsValid(ShootMode) && IsValid(ControllerModeMgr))
				{
					TArray<FString> OtherValue = ControllerModeMgr->GetOtherValue();
					FString StateName = ShootMode->GetStateType();
					if ((!StateName.Compare("YCJMD")) || (!StateName.Compare("HSBZ")))
					{
						int32 SizeX = 0, SizeY = 0;
						PlayerController->GetViewportSize(SizeX, SizeY);
						FHitResult TraceHitResult;
						FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true);
						TraceParams.bTraceComplex = true;
						TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
						PlayerController->GetHitResultAtScreenPosition(FVector2D(SizeX / 2.0f, SizeY / 2.0f), PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
						if (TraceHitResult.bBlockingHit)
						{
							PlayerActor->OnSimulateMouseLeftButtonClick(TraceHitResult.ImpactPoint);
						}
						else
						{
							FVector WorldOrigin;
							FVector WorldDirection;
							if (UGameplayStatics::DeprojectScreenToWorld(PlayerController, FVector2D(SizeX / 2.0f, SizeY / 2.0f), WorldOrigin, WorldDirection) == true)
							{
								PlayerActor->OnSimulateMouseLeftButtonClick(WorldOrigin + WorldDirection * 5000.0f);
								return;
							}
						}
					}
				}
			}
		}
	}
}
#pragma endregion

#pragma region 使用射击连线技能（射击左键按下操作）
void UUseSkillOfLineShoot::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUseSkillOfLineShoot_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}

	int32 TargetID = UGolbalBPFunctionLibrary::GetTargetEntityID();

	OtherValue.Empty();

	if (UGolbalBPFunctionLibrary::GetPlayerID() == TargetID)
	{
		FString SkillID = GetSkillIDByState( 2);
		if (SkillID.IsEmpty())return;
		OtherValue.Add(SkillID);
		OtherValue.Add(TEXT("0"));
	}
	else
	{
		FString SkillID = GetSkillIDByState( 3);
		if (SkillID.IsEmpty())return;
		OtherValue.Add(SkillID);
		OtherValue.Add(INT_TO_FSTRING(TargetID));
	}


	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UUseSkillOfLineShoot::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}

	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UUseSkillOfLineShoot::IsCanExecuteOperation: PlayerController!"));
		return false;
	}

	bool IsMouseYDown = PlayerController->IsInputKeyDown(EKeys::RightMouseButton);

	if (!IsMouseYDown)
	{
		return false;
	}

	return true;
}

#pragma endregion

#pragma region 打断射击连线技能（射击右键按下操作）
void UBreakSkillOfLineShoot::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBreakSkillOfLineShoot_ExecuteOperation);
	FString SkillID = GetSkillIDByState(4);
	if (SkillID.IsEmpty())return;
	OtherValue.Empty();
	OtherValue.Add(SkillID);
	OtherValue.Add(TEXT("0"));
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}
#pragma endregion

#pragma region 关闭射击技能（射击左键释放操作）
void UCloseAutoShoot::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	if (!IsCanExecuteOperation())
	{
		return;
	}

	UGolbalBPFunctionLibrary::GEventManager()->OnCloseAutoShoot.ExecuteIfBound();
}
#pragma endregion


#pragma region 右键瞄准状态（远程吃鸡）
void UUseAimState::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	//远程吃鸡右键功能表现
	if (IsValid(PlayerActor) && PlayerActor->bIsYCJMDCopy)
	{
		PlayerActor->OnClickRightMouseYCJMD();
	}
}
#pragma endregion

#pragma region 切换自动寻路
void UActivateNavigateMoveMode::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UActivateNavigateMoveMode_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//不能移动则禁用
	if (IsValid(PlayerController) && OtherValue.Num() > 6)
	{
		FVector DstPosition = UGolbalBPFunctionLibrary::FStringToFVector(OtherValue[0]);
		PlayerController->GetAtkStateMar()->SwitchNavigateMoveMode
		(true, DstPosition, FSTRING_TO_FLOAT(OtherValue[1]), OtherValue[2], FSTRING_TO_INT(OtherValue[3]), FSTRING_TO_INT(OtherValue[4]) == 1, FSTRING_TO_INT(OtherValue[5]) == 1, FSTRING_TO_INT(OtherValue[6]));
	}
}

bool UActivateNavigateMoveMode::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	//不能移动则禁用
	if (IsValid(PlayerController) && !PlayerController->CanMoveControl())
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->MessageManager))
		{
			//当玩家受到影响移动的开关限制时，无法寻路.
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(2412);
		}
		return false;
	}
	return true;
}
#pragma endregion

#pragma region 切出自动寻路
void UUnActivateNavigateMoveMode::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UUnActivateNavigateMoveMode_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()) && OtherValue.Num() > 5)
	{
		FVector DstPosition = UGolbalBPFunctionLibrary::FStringToFVector(OtherValue[0]);
		PlayerController->GetAtkStateMar()->SwitchNavigateMoveMode
		(false, DstPosition, FSTRING_TO_FLOAT(OtherValue[1]), OtherValue[2], FSTRING_TO_INT(OtherValue[3]), FSTRING_TO_INT(OtherValue[4]) == 1, FSTRING_TO_INT(OtherValue[5]) == 1, FSTRING_TO_INT(OtherValue[6]));
	}
}
#pragma endregion

#pragma region 开始跨地图寻路
void UStartCrossMapNavigate::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UStartCrossMapNavigate_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	FString DstSpace = TEXT("");
	bool IsCompleted = false;
	FString QuestTaskClass = "";
	FString NPCScriptID = "";
	FVector FinalPosition = FVector::ZeroVector;
	float NearbyRange = 2.0f;
	int AutoQuestID = 0;
	int32 GossipWithType = 0;
	ENUM_NAVIGATE_ACTION_TYPE NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault;
	if (OtherValue.Num() > 0)
	{
		DstSpace = OtherValue[0];
	}
	if (OtherValue.Num() > 1)
	{
		IsCompleted = FSTRING_TO_INT(OtherValue[1]) == 1 ? true : false;
	}
	if (OtherValue.Num() > 2)
	{
		QuestTaskClass = OtherValue[2];
	}
	if (OtherValue.Num() > 3)
	{
		NPCScriptID = OtherValue[3];
	}
	if (OtherValue.Num() > 4)
	{
		TArray<FString> FinalPositions = UGolbalBPFunctionLibrary::SplitString(OtherValue[4]);
		if (FinalPositions.Num() > 2)
		{
			FinalPosition = FVector(FSTRING_TO_FLOAT(FinalPositions[0]), FSTRING_TO_FLOAT(FinalPositions[1]), FSTRING_TO_FLOAT(FinalPositions[2]));
		}
	}
	if (OtherValue.Num() > 5)
	{
		NearbyRange = FSTRING_TO_FLOAT(OtherValue[5]);
	}
	if (OtherValue.Num() > 6)
	{
		AutoQuestID = FSTRING_TO_INT(OtherValue[6]);
	}
	if (OtherValue.Num() > 7)
	{
		if (FSTRING_TO_INT(OtherValue[7]) == 0)
		{
			NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionDefault;
		}
		else if (FSTRING_TO_INT(OtherValue[7]) == 1)
		{
			NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionStall;
		}
		else if (FSTRING_TO_INT(OtherValue[7]) == 2)
		{
			NavigateActionType = ENUM_NAVIGATE_ACTION_TYPE::NavigateActionCrond;
		}
	}
	if (OtherValue.Num() > 8)
	{
		GossipWithType = FSTRING_TO_INT(OtherValue[8]);
	}
	//获取玩家
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->StartCrossMapNavigate(DstSpace, IsCompleted, QuestTaskClass, NPCScriptID, FinalPosition, NearbyRange, AutoQuestID, NavigateActionType, GossipWithType);
	}
}
#pragma endregion

#pragma region 开始摆摊
void UOnStartStallOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	if (!IsCanExecuteOperation())
	{
		return;
	}
	URoleStallInterface * RoleStallInterface = Cast<URoleStallInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface"), 0));
	if (IsValid(RoleStallInterface))
	{
		RoleStallInterface->FindStallPoint();
	}
}
#pragma endregion

#pragma region	八卦阵向前移动操作基类
void UBaGuaZhenForwardMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaGuaZhenForwardMoveOperation_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		APawn* PlayerCharacter = PlayerController->GetPawn();
		if (IsValid(PlayerCharacter))
		{
			float MoveScale = 0.0f;
			if (IsValid(PlayerController->GetAtkStateMar()))
			{
				MoveScale = PlayerController->GetAtkStateMar()->GetBaGuaZhenModeValue();
			}
			FVector OffsetOffset = UKismetMathLibrary::GetForwardVector(FRotator::ZeroRotator) * InputScale * MoveScale;
 			PlayerCharacter->AddActorWorldOffset(OffsetOffset, true);
		}
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UBaGuaZhenForwardMoveOperation::IsCanExecuteOperation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
		if (IsValid(AtkStateMar))
		{
			return AtkStateMar->GetBaGuaZhenModeCanMove();
		}
	}
	return false;
}

#pragma endregion

#pragma region	八卦阵向右移动操作基类
void UBaGuaZhenRightMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	SCOPE_CYCLE_COUNTER(STAT_UBaGuaZhenRightMoveOperation_ExecuteOperation);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController))
	{
		APawn* PlayerCharacter = PlayerController->GetPawn();
		if (IsValid(PlayerCharacter))
		{
			float MoveScale = 0.0f;
			if (IsValid(PlayerController->GetAtkStateMar()))
			{
				MoveScale = PlayerController->GetAtkStateMar()->GetBaGuaZhenModeValue();
			}
			FVector OffsetOffset = UKismetMathLibrary::GetRightVector(FRotator::ZeroRotator) * InputScale * MoveScale;
			PlayerCharacter->AddActorWorldOffset(OffsetOffset, true);
		}
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UBaGuaZhenRightMoveOperation::IsCanExecuteOperation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
		if (IsValid(AtkStateMar))
		{
			return AtkStateMar->GetBaGuaZhenModeCanMove();
		}
	}
	return false;
}

#pragma endregion

void UMiJingForwardOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	if (!IsCanExecuteOperation())
	{
		return;
	}
	//获取玩家
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//操作模式管理器
	UOperationModeMgr* OperationModeMgr = UGolbalBPFunctionLibrary::OperationModeMgr();
	//获取玩家控制器
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(PlayerController) || !IsValid(OperationModeMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseMoveOperation::ExecuteOperation : PlayerController || OperationModeMgr!"));
		return;
	}

	//获取玩家控制转向
	FRotator ControlRotator = PlayerActor->GetActorRotation();

	//移动轴值记录
	float Scale = InputScale;

	//判断是否为自动移动
	if (OperationModeMgr->bIsAutoMove)
	{
		USkillInterface* SkillInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.SkillInterface : nullptr;
		if (IsValid(SkillInterface))
		{
			Scale = SkillInterface->MoveScale;
			if (SkillInterface->DstRotation != FRotator::ZeroRotator )
			{
				ControlRotator = SkillInterface->DstRotation;
			}

		}
	}
	//获取相对玩家的前方向
	FVector ForwardByPlayer = UKismetMathLibrary::GetForwardVector(FRotator(ControlRotator.Pitch, ControlRotator.Yaw, 0.0f));
	//获取飞行状态下相对于玩家前
	FVector ForwardByFlyPlayer = ForwardByPlayer;
	//获取被记录的向量
	FVector KeepVector = OperationModeMgr->ForwardVector;

	//是否保持方向不变
	if (OperationModeMgr->bIsKeepDirection)
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(KeepVector, Scale);
	}
	else if (PlayerController->IsFlying())//飞行状态
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(ForwardByFlyPlayer, Scale);
	}
	else
	{
		//添加移动数据到数组
		PlayerController->AddMovementArray(ForwardByPlayer, Scale);
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UMiJingForwardOperation::IsCanExecuteOperation()
{
	bool IsCanExecute= Super::IsCanExecuteOperation();
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if ((!IsValid(PlayerController) || !PlayerController->CanMoveControl())&& !IsCanExecute)
	{
		return true;
	}
	return IsCanExecute;
}

void UPlayerLedgesJumpOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerActor))
	{
		int32 LedgesJumpDownStep = 2;
		GetParameter(LedgesJumpDownStep);
		PlayerActor->LedgesJumpDownStep = LedgesJumpDownStep;
		PlayerActor->ExecuteLedgesJump();
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

void UPlayerLedgesJumpOperation::GetParameter(int32& LedgesJumpDownStep)
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();
	if (IsValid(ControllerModeMgr) && IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()))
	{
		UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
		if (IsValid(AtkStateMar))
		{
			UAtkStateBase* ShootAtkState = AtkStateMar->GetCurAtkState();
			if (IsValid(ShootAtkState))
			{
				FString TypStr = "";
				if (ShootAtkState->GetAttState() == EATTACT_STATE::BEHAVIOR_MIJING)
				{
					TypStr = "MiJing";
				}
				else
				{
					TypStr = "";
				}

				TArray<FString> OtherValue = ControllerModeMgr->GetOtherValue();
				for (FString data : OtherValue)
				{
					TArray<FString> StateData = UGolbalBPFunctionLibrary::SplitString(data, true);
					if (StateData.Num() <= 0)
					{
						break;
					}
					if (!StateData[0].Compare(TypStr))
					{
						if (StateData.IsValidIndex(1))
						{
							LedgesJumpDownStep = FSTRING_TO_INT(StateData[1]);
						}
						if (StateData.IsValidIndex(2))
						{
							//LedgesJumpDownStep = FSTRING_TO_INT(StateOtherValueData[2]);
						}
					}
				}
			}
		}
	}
}

#pragma region 云梯上下攀爬
void ULadderForwardMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->LadderCustomMovmentCpt->AddMovementLadderUp(InputScale);
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}
#pragma endregion

#pragma region 控制的Pawn的移动操作基类
void UBaseActorMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (!IsCanExecuteOperation())
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(28);
		return;
	}
	//获取玩家控制器控制的Pawn
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor) || FMath::IsNearlyZero(InputScale))
	{
		return;
	}
	
	FVector MoveDirection = FVector::ZeroVector;

	//获取移动朝向向量数据
	if (!GetMoveWorldDirection(MoveDirection))
	{
		return;
	}

	//移动轴值记录
	float Scale = InputScale;
	ControlActor->AddMovementInput(MoveDirection, Scale);
}

bool UBaseActorMoveOperation::GetMoveWorldDirection(FVector& MoveVector)
{

	return true;
}

bool UBaseActorMoveOperation::IsCanExecuteOperation()
{
	return true;
}
#pragma endregion

#pragma region	玩家控制器控制的Pawn前后左右方向移动操作
bool UActorMoveForwardOperation::GetMoveWorldDirection(FVector& MoveVector)
{
	//获取玩家控制器控制的Pawn转向
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return false;
	}
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor))
	{
		return false;
	}
	FRotator ControlRotator = ControlActor->GetControlRotation();
	//获取相对玩家的前方向
	MoveVector = UKismetMathLibrary::GetForwardVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//MoveVector = ControlActor->GetActorForwardVector();
	return true;
}

bool UActorMoveForwardOperation::IsCanExecuteOperation()
{
	return true;
}

bool UActorMoveRightOperation::GetMoveWorldDirection(FVector& MoveVector)
{
	//获取玩家控制器控制的Pawn转向
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return false;
	}
	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
	if (!IsValid(ControlActor))
	{
		return false;
	}
	FRotator ControlRotator = ControlActor->GetControlRotation();

	//获取相对玩家的右方向
	MoveVector = UKismetMathLibrary::GetRightVector(FRotator(0.0f, ControlRotator.Yaw, 0.0f));
	//MoveVector = ControlActor->GetActorRightVector();
	return true;
}

bool UActorMoveRightOperation::IsCanExecuteOperation()
{
	return true;
}
#pragma endregion

#pragma region	玩家控制器控制的Pawn前后左右左右方向移动操作(多人载具)
bool UActorMoveForwardOperation_Vehicle::GetMoveWorldDirection(FVector& MoveVector)
{
	return Super::GetMoveWorldDirection(MoveVector);
}

bool UActorMoveForwardOperation_Vehicle::IsCanExecuteOperation()
{
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		if (Interface->HasVehicle() && !Interface->IsVehicleDriver())
		{
			//玩家是乘客不能移动
			return false;
		}
	}
	return true;
}

bool UActorMoveRightOperation_Vehicle::GetMoveWorldDirection(FVector& MoveVector)
{
	return Super::GetMoveWorldDirection(MoveVector);
}

bool UActorMoveRightOperation_Vehicle::IsCanExecuteOperation()
{
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		if (Interface->HasVehicle() && !Interface->IsVehicleDriver())
		{
			//玩家是乘客不能移动
			return false;
		}
	}
	return true;
}
#pragma endregion

#pragma region	玩家控制器控制的Pawn旋转操作
void UActorTurnOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
// 	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
// 
// 	//获取玩家
// 	AServerCharacter* ControlActor = Cast<AServerCharacter>(PlayerController->GetPawn());
// 	if (!IsValid(ControlActor))
// 	{
// 		return;
// 	}
// 
// 	if (!IsCanExecuteOperation())
// 	{
// 		ControlActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
// 		ControlActor->bUseControllerRotationYaw = false;
// 		return;
// 	}
// 
// 	//获取当前移动方向
// 	FVector MoveVector = ControlActor->GetVelocity();
// 	//获取旋转
// 	float CurRotate = ControlActor->GetActorRotation().Yaw;
// 	//获取玩家移动方向旋转值
// 	float MoveRotate = MoveVector.Rotation().Yaw;
// 	//计算旋转值的差
// 	float Tem = UKismetMathLibrary::FFloor((MoveRotate - CurRotate + 180.0f) / 360.0f) * 360.0f;
// 	float RotateVaule = MoveRotate - CurRotate - Tem;
// 
// 	//设置到玩家数据里
// 	ControlActor->GetCharacterMovement()->RotationRate.Yaw = 0.0f;
// 	ControlActor->bUseControllerRotationYaw = true;
}

bool UActorTurnOperation::IsCanExecuteOperation()
{
	return true;
}
#pragma endregion

void UUseQuickKeyOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	int32 QuickKeyIndex = FSTRING_TO_INT(OtherValue[0]);
	PlayerController->UseQuickKey(QuickKeyIndex);
}

void UShootYCJMDUseQuickKeyOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		return;
	}
	//快捷键
	int32 QuickKeyIndex = FSTRING_TO_INT(OtherValue[0]);
	//换算成格子索引
	int32 QuickSlotIndex;
	if (QuickKeyIndex == 0)
	{
		QuickSlotIndex = 9;
	}
	else
	{
		QuickSlotIndex = QuickKeyIndex - 1;
	}
	URoleSpaceContentInterface * RoleSpaceContentInterface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (IsValid(RoleSpaceContentInterface) && RoleSpaceContentInterface->YCJMDQuickBarItems.Num()>0 && RoleSpaceContentInterface->YCJMDQuickBarItems.Contains(QuickSlotIndex))
	{
		FQB_ITEM QB_ITEM =RoleSpaceContentInterface->YCJMDQuickBarItems.FindRef(QuickSlotIndex);
		if (QB_ITEM.QbType == UUECS3GameInstance::Instance->ConstDataBP->QB_ITEM_SKILL || QB_ITEM.QbType == UUECS3GameInstance::Instance->ConstDataBP->QB_ITEM_PET_SHENTONG_SKILL)
		{
			if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
			{
				TArray<FString> UseSkillOtherValue;
				UseSkillOtherValue.Add(INT_TO_FSTRING(QB_ITEM.CurrQbID));
				int32 TargetID = UGolbalBPFunctionLibrary::GetTargetEntityID();				
				if (UGolbalBPFunctionLibrary::GetPlayerID() == TargetID)
				{
					UseSkillOtherValue.Add(TEXT("0"));
				}
				else
				{
					UseSkillOtherValue.Add(INT_TO_FSTRING(TargetID));
				}
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("UseSkill"), TEXT(""), 0.0f, UseSkillOtherValue);
			}
		}
		else if (QB_ITEM.QbType == UUECS3GameInstance::Instance->ConstDataBP->QB_ITEM_KITBAG)
		{
			if (IsValid(UGolbalBPFunctionLibrary::ControllerModeMgr()))
			{
				TArray<FString> UseItemInQuickOtherValue;
				UseItemInQuickOtherValue.Add(TEXT("607"));
				UseItemInQuickOtherValue.Add(INT_TO_FSTRING(QB_ITEM.CurrQbID));
				UseItemInQuickOtherValue.Add(INT_TO_FSTRING(QB_ITEM.BindType));
				UGolbalBPFunctionLibrary::ControllerModeMgr()->ExecuteInputInfor(TEXT("UseItemInQuick"), TEXT(""), 0.0f, UseItemInQuickOtherValue);
			}
		}
	}	
}

void UEquipBuildLeftClickOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);

	if (!IsCanExecuteOperation())
	{
		return;
	}

	//获取玩家
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEquipBuildLeftClickOperation::ExecuteOperation : PlayerActor!"));
		return;
	}

	FString ScriptID = TEXT("");
	FString ItemUID = TEXT("");
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
	if (IsValid(AtkStateMar))
	{
		ScriptID = AtkStateMar->GetEquipScriptID();
		ItemUID = AtkStateMar->GetEquipItemUID();
	}
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (IsValid(Interface))
	{
		Interface->RequestCreateApparatus(ScriptID, ItemUID);
	}
}

void UEquipBuildCancelOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	if (!IsCanExecuteOperation())
	{
		return;
	}
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		return Interface->OnLeaveEquipBuild();
	}
}

void UYCJMDSkyCarrierRightMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController) && !IsValid(PlayerCharacter))
	{
		return;
	}

	if (InputScale != 0.0f)
	{
		FRotator ControlRotation = PlayerController->GetControlRotation();
		FRotator TargetRotation = PlayerCharacter->GetActorRotation();
		TargetRotation.Pitch = ControlRotation.Pitch;
		TargetRotation.Roll = ControlRotation.Roll;
		PlayerController->SetControlRotation(FMath::RInterpTo(ControlRotation, TargetRotation, 0.07f, 0.5f));
	}
}

void ULeaveYCJMDSkyCarrierOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerCharacter) || !IsValid(PlayerCharacter->FlyPatrolComponent))
	{
		return;
	}
	PlayerCharacter->FlyPatrolComponent->LeaveSkyCarrierKeyF();
}

void UYCJMDFKeyOpenParachuteOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerCharacter) || !IsValid(PlayerCharacter->FlyPatrolComponent))
	{
		return;
	}
	PlayerCharacter->FlyPatrolComponent->OpenYCJMDParachuteKeyF();
}

void UYCJMDSkyDivingForwardMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (IsValid(PlayerController) && IsValid(PlayerCharacter))
	{
		if (PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_OPEN))return;

		float VelZ = PlayerCharacter->GetCharacterMovement()->Velocity.Z;

		//请特别注意：我们项目中此函数传递的InputScale值当按下WD时，并不是一直是1111111发送，而是10101010这样的发送的，则需要判断WASD按键按下的时长
		FGROUPKEY_DATA MoveForwardKeyValue;
		FGROUPKEY_DATA MoveBackKeyValue;
		PlayerController->GetKeyNameByActName(TEXT("MoveForward"), MoveForwardKeyValue);
		PlayerController->GetKeyNameByActName(TEXT("MoveBack"), MoveBackKeyValue);		
		float MoveForwardKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveForwardKeyValue.Key);
		float MoveBackKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveBackKeyValue.Key);

		if (MoveForwardKeyTimeDown > 0.0f)
		{
			VelZ -= 40.0f;//W键则加速向下，每帧的加速度步长
			PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY < 50.f ? PlayerCharacter->YCJMDParachuteDirY + 1 : 50.f;

			FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorForwardVector());
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 3000.0f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 3000.0f;
		}
		else  if (MoveBackKeyTimeDown > 0.0f)
		{
			VelZ = FMath::Min(VelZ + 10.0f, -4500.0f);
			PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY > -50.f ? PlayerCharacter->YCJMDParachuteDirY - 1: -50.f;
		}
		else
		{
			VelZ -= 30.0f;
			if (PlayerCharacter->YCJMDParachuteDirY != 0.0f)
			{
				if (PlayerCharacter->YCJMDParachuteDirY > 0.0f)
				{
					PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY - 0.5;
				}
				else
				{
					PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY + 0.5;
				}
			}
			FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorForwardVector());
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 2000.0f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 2000.0f;
		}

		VelZ = FMath::Max(VelZ, -5000.0f);
		PlayerCharacter->GetCharacterMovement()->Velocity.Z = VelZ;
	}
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);
}

void UYCJMDSkyDivingRightMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	UBaseOperation::ExecuteOperation(InputKey, InputScale, OtherValue);

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(PlayerController) && IsValid(PlayerCharacter))
	{
		if (PlayerCharacter->IsParachuteState(PARACHUTE_STATE::PARACHUTE_STATE_OPEN))return;

		FGROUPKEY_DATA MoveRightKeyValue;
		FGROUPKEY_DATA MoveLeftKeyValue;
		PlayerController->GetKeyNameByActName(TEXT("MoveRight"), MoveRightKeyValue);
		PlayerController->GetKeyNameByActName(TEXT("MoveLeft"), MoveLeftKeyValue);
		float MoveRightKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveRightKeyValue.Key);
		float MoveLeftKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveLeftKeyValue.Key);

		if (MoveRightKeyTimeDown > 0.0f )
		{
			PlayerCharacter->YCJMDParachuteDirX = PlayerCharacter->YCJMDParachuteDirX < 50.f ? PlayerCharacter->YCJMDParachuteDirX + 1 : 50.f;

			FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorRightVector());
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 2000.f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 2000.f;
		}
		else if (MoveLeftKeyTimeDown > 0.0f)
		{
			PlayerCharacter->YCJMDParachuteDirX = PlayerCharacter->YCJMDParachuteDirX > -50.f ? PlayerCharacter->YCJMDParachuteDirX - 1 : -50.f;

			FRotator ComposeRotator = UKismetMathLibrary::ComposeRotators(PlayerCharacter->GetActorRotation(), FRotator(0.f, -90.f, 0.f));
			FVector PlayerVector = UKismetMathLibrary::Normal(UKismetMathLibrary::GetForwardVector(ComposeRotator));
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 2000.f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 2000.f;
		}
		else
		{
			if (MoveRightKeyTimeDown <= 0.0f || MoveLeftKeyTimeDown <= 0.0f)
			{
				if (PlayerCharacter->YCJMDParachuteDirX != 0.0f)
				{
					PlayerCharacter->bUseControllerRotationYaw = false;
					if (PlayerCharacter->YCJMDParachuteDirX > 0.f)
					{
						PlayerCharacter->YCJMDParachuteDirX -= 0.5;
					}
					else
					{
						PlayerCharacter->YCJMDParachuteDirX += 0.5;
					}
				}
			}
			
			
		}
	}
}

void UYCJMDOpenParachuteForwardMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController) && !IsValid(PlayerCharacter))
	{
		return;
	}

	float VelZ = PlayerCharacter->GetCharacterMovement()->Velocity.Z;

	//请特别注意：我们项目中此函数传递的InputScale值当按下WD时，并不是一直是1111111发送，而是10101010这样的发送的，则需要判断WASD按键按下的时长
	FGROUPKEY_DATA MoveForwardKeyValue;
	FGROUPKEY_DATA MoveBackKeyValue;
	PlayerController->GetKeyNameByActName(TEXT("MoveForward"), MoveForwardKeyValue);
	PlayerController->GetKeyNameByActName(TEXT("MoveBack"), MoveBackKeyValue);
	float MoveForwardKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveForwardKeyValue.Key);
	float MoveBackKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveBackKeyValue.Key);

	if (MoveForwardKeyTimeDown > 0.0f && InputScale > 0.0f)
	{
		VelZ = FMath::Max(-2000.f, VelZ - 20.0f);//W键则加速向下，每帧的加速度步长
		PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY < 50.f ? PlayerCharacter->YCJMDParachuteDirY + 0.5 : 50.f;

		FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorForwardVector());
		PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 1500.f;
		PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 1500.f;
	}
	else  if (MoveBackKeyTimeDown > 0.0f && InputScale < 0.0f)
	{
		//S键则减速向下，每帧的加速度步长
		VelZ = FMath::Min(-800.f, VelZ + 10.0f);
		PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY > -50.f ? PlayerCharacter->YCJMDParachuteDirY - 0.5 : -50.f;
	}
	else
	{
		//当AD键也未按下的时则判定为自由下落
		if (MoveForwardKeyTimeDown <= 0.0f && MoveBackKeyTimeDown <= 0.0f)
		{
			if (VelZ != -1000.0f)
			{
				VelZ = VelZ < -1000.f ? FMath::Min(-1000.f, VelZ + 6.0f) : FMath::Max(-1000.f, VelZ - 6.0f);
			}

			if (PlayerCharacter->YCJMDParachuteDirY != 0.0f)
			{
				if (PlayerCharacter->YCJMDParachuteDirY > 0)
				{
					PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY - 0.5;
				}
				else
				{
					PlayerCharacter->YCJMDParachuteDirY = PlayerCharacter->YCJMDParachuteDirY + 0.5;
				}

			}
		}
		FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorForwardVector());
		PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 900.f;
		PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 900.f;
	}

	PlayerCharacter->GetCharacterMovement()->Velocity.Z = VelZ;

	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}

void UYCJMDOpenParachuteRightMoveOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerCharacter))
	{
		FGROUPKEY_DATA MoveRightKeyValue;
		FGROUPKEY_DATA MoveLeftKeyValue;
		PlayerController->GetKeyNameByActName(TEXT("MoveRight"), MoveRightKeyValue);
		PlayerController->GetKeyNameByActName(TEXT("MoveLeft"), MoveLeftKeyValue);
		float MoveRightKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveRightKeyValue.Key);
		float MoveLeftKeyTimeDown = PlayerController->GetInputKeyTimeDown(MoveLeftKeyValue.Key);

		if (MoveRightKeyTimeDown > 0 && InputScale > 0.0f)
		{
			PlayerCharacter->YCJMDParachuteDirX = PlayerCharacter->YCJMDParachuteDirX < 50.f ? PlayerCharacter->YCJMDParachuteDirX + 1 : 50.f;

			FVector PlayerVector = UKismetMathLibrary::Normal(PlayerCharacter->GetActorRightVector());
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 1500.f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 1500.f;

			PlayerCharacter->AddControllerYawInput(PlayerCharacter->YCJMDParachuteDirX / 50.f * 0.3);
			PlayerCharacter->bUseControllerRotationYaw = true;
		}
		else if(MoveLeftKeyTimeDown > 0 && InputScale < 0.0f)
		{
			PlayerCharacter->YCJMDParachuteDirX = PlayerCharacter->YCJMDParachuteDirX > -50.f ? PlayerCharacter->YCJMDParachuteDirX - 1 : -50.f;

			FRotator ComposeRotator = UKismetMathLibrary::ComposeRotators(PlayerCharacter->GetActorRotation(), FRotator(0.f, -90.f, 0.f));
			FVector PlayerVector = UKismetMathLibrary::Normal(UKismetMathLibrary::GetForwardVector(ComposeRotator));
			PlayerCharacter->GetCharacterMovement()->Velocity.X = PlayerVector.X * 1500.f;
			PlayerCharacter->GetCharacterMovement()->Velocity.Y = PlayerVector.Y * 1500.f;

			PlayerCharacter->AddControllerYawInput(PlayerCharacter->YCJMDParachuteDirX / 50.f * 0.3);
			PlayerCharacter->bUseControllerRotationYaw = true;
		}
		else
		{
			if (MoveLeftKeyTimeDown <= 0 && MoveRightKeyTimeDown <= 0)
			{
				if (PlayerCharacter->YCJMDParachuteDirX != 0.0f)
				{
					PlayerCharacter->bUseControllerRotationYaw = false;
					if (PlayerCharacter->YCJMDParachuteDirX > 0.f)
					{
						PlayerCharacter->YCJMDParachuteDirX -= 0.5;
					}
					else
					{
						PlayerCharacter->YCJMDParachuteDirX += 0.5;
					}
				}
			}
			
		}
	}
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
}

bool UVehicleOperation::IsCanExecuteOperation()
{
	if (!Super::IsCanExecuteOperation())
	{
		return false;
	}
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		return Interface->HasVehicle();
	}
	return false;
}

void UVehicleOperation::ExecuteOperation(FString InputKey, const float& InputScale, TArray<FString> OtherValue)
{
	Super::ExecuteOperation(InputKey, InputScale, OtherValue);
	//单人骑乘
	URolePetInterface* RolePetInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), 0));

	if (IsValid(RolePetInterface))
	{
		RolePetInterface->RequestTransformPetFC();
	}

	if (!IsCanExecuteOperation())
	{
		return;
	}
	//多人载具
	URoleSpaceContentInterface* Interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (Interface)
	{
		return Interface->CELL_dismountVehicle();
	}
}
CONTROL_COMPILE_OPTIMIZE_END

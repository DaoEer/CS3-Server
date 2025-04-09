// Fill out your copyright notice in the Description page of Project Settings.

#include "JumpComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
//CS3数据
#include "GameData/RoleJumpData.h"
#include "GameData/GameDeFine.h"
//CS3
#include "GameData/ConstData.h"
#include "Util/CS3Debug.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/SkillInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/SkillManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleStateInterface.h"
#include "Util/ConvertUtil.h"
#include "Kismet/KismetSystemLibrary.h"
#include "NavigationSystem.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/GameStatus.h"

DECLARE_CYCLE_STAT(TEXT("InitComponent"), STAT_InitComponent, STATGROUP_UJumpComponent);
DECLARE_CYCLE_STAT(TEXT("OnCheckJumpSkill"), STAT_OnCheckJumpSkill, STATGROUP_UJumpComponent);
DECLARE_CYCLE_STAT(TEXT("SetJumpMaxCountBySkill"), STAT_SetJumpMaxCountBySkill, STATGROUP_UJumpComponent);

CONTROL_COMPILE_OPTIMIZE_START
// Sets default values for this component's properties
UJumpComponent::UJumpComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UJumpComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UJumpComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	if (PlayerCharacter->GetSelfEntity() == nullptr)
	{
		return;
	}

	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (PlayerCharacter->IsJumpParachuteState())
	{
		return;
	}

	if (PlayerCharacter->ActorIsPlayer())
	{
		CheckJumpFalling();
	}
	/*CS3_Display(CS3DebugType::CL_Undefined, TEXT("PADDDOWUXIAN=======IsTheUping=%d,    IsTheFalling=%d,"),
			IsTheUping?1:0, IsTheFalling?1:0);*/
}

void UJumpComponent::InitJumpData()
{
	SCOPE_CYCLE_COUNTER(STAT_InitComponent);

	GetOwnerCharacter()->GetCharacterMovement()->MaxStepHeight = 100.0f;
	GetOwnerCharacter()->GetCharacterMovement()->SetWalkableFloorAngle(80);

	PlayerJumpMaxCount = 0;
	GetOwnerCharacter()->JumpMaxCount = 99999999;//使用PlayerJumpMaxCount代替判断，不用引擎的CanJump()
}

void UJumpComponent::OnStartActiveJump()
{
	SCOPE_CYCLE_COUNTER(STAT_OnCheckJumpSkill);
	if (!IsCanJump())
	{
		return;
	}

	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	int32 JumpCurrentCount = GetOwnerCharacter()->JumpCurrentCount;
	//int32 JumpMaxCount = GetOwnerCharacter()->JumpMaxCount;
	bool bIsActiveMoveing = PlayerCharacter->IsActiveMoveing();
	JUMP_SHOW_STATE JumpType = JUMP_SHOW_STATE::JUMP_SHOW_STATE_STAND;
	float JumpHeight = 0.0f;

	if (JumpCurrentCount == 0)
	{
		if (!bIsActiveMoveing)
		{
			JumpType = JUMP_SHOW_STATE::JUMP_SHOW_STATE_SJUMP;
			JumpHeight = ONE_JUMP_HEIGHT;
		}
		else
		{
			JumpType = JUMP_SHOW_STATE::JUMP_SHOW_STATE_MJUMP;
			JumpHeight = LedgesJumpHeight > 0.0f ? LedgesJumpHeight:ONE_JUMP_HEIGHT;///当有边缘辅助起跳时，优先用辅助跳高度
			LedgesJumpHeight = 0.0f;
		}
	}
	else if (JumpCurrentCount == 1)
	{
		JumpType = JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_SJUMP;
		JumpHeight = TWO_JUMP_HEIGHT;
	}
	else if (JumpCurrentCount == 2)
	{
		JumpType = JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_SJUMP;
		JumpHeight = THREE_JUMP_HEIGHT;
	}

	//防止二段、三段跳的时候再次缓存导致错误
	if (!IsJumpState)
	{
		PlayerCharacter->SetCharacterMoveCacheData();///缓存重力系数
	}

	IsJumpState = true;
	IsTheLand = false;
	PlayerCharacter->SetBaseGravityScale(1.0f);
	SetJumpHeight(JumpHeight);
	PlayerCharacter->Jump();
	ChangeJumpStateToServer(JumpType);
}

void UJumpComponent::OnStartPassiveJump(float Height)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	//防止二段、三段跳的时候再次缓存导致错误
	if (!IsJumpState)
	{
		PlayerCharacter->SetCharacterMoveCacheData();///缓存重力系数
	}
	IsJumpState = true;
	IsTheLand = false;
	PlayerCharacter->SetBaseGravityScale(1.0f);
	SetJumpHeight(Height);
	PlayerCharacter->Jump();
	ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_PASSIVE);
}

void UJumpComponent::SetJumpMaxCountBySkill()
{
	SCOPE_CYCLE_COUNTER(STAT_SetJumpMaxCountBySkill);
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return;
	}

	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}

	if (PlayerCharacter->IsRidePetState())
	{
		PlayerJumpMaxCount = 1;
	}
	else
	{
		TArray<int32> SkillIDList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
		TArray<int32> ForbidJumpSkillIDs = UUECS3GameInstance::Instance->SkillManager->GetForbidJumpSkillIDs();
		if (SkillIDList.Contains(THREE_SECTION_JUMP_SKILLID) && !ForbidJumpSkillIDs.Contains(THREE_SECTION_JUMP_SKILLID) && 
			!ForbidJumpSkillIDs.Contains(TWO_SECTION_JUMP_SKILLID))
		{
			PlayerJumpMaxCount = 3;
			return;
		}
		else if (SkillIDList.Contains(TWO_SECTION_JUMP_SKILLID) && !ForbidJumpSkillIDs.Contains(TWO_SECTION_JUMP_SKILLID))
		{
			PlayerJumpMaxCount = 2;
			return;
		}
		PlayerJumpMaxCount = 1;
	}
}

void UJumpComponent::ChangeJumpStateToServer(JUMP_SHOW_STATE JumpState)
{
	if (CurJumpShowState == JumpState)
	{
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UJumpComponent::ChangeJumpStateToServer[CurJumpShowState=%d, NewJumpState=%d]"), 
		(int32)CurJumpShowState, (int32)JumpState);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
	CurJumpShowState = JumpState;
	 
	//获取本地控制的玩家的interface[0表示是控制玩家]
	URoleStateInterface* RoleStateInterface = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr);
	if(IsValid(RoleStateInterface))
	{
		RoleStateInterface->UpdateJumpState(JumpState);///更新自己的客户端跳跃表现
		RoleStateInterface->RequestChangeJumpState(JumpState);///通知服务器更新其他客户端本机主角的表现
	}
}

void UJumpComponent::ResetJumpCount()
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	if (PlayerCharacter->JumpCurrentCount != 0)
	{
		PlayerCharacter->JumpCurrentCount = 0;
	}
}

void UJumpComponent::MovementModeChanged(EMovementMode PrevMovementMode, uint8 PreviousCustomMode /*= 0*/)
{
	APlayerCharacter *PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	CHANGE_CHARACTER_MOVEMENT_TYPE ChangeMovementType = CHANGE_CHARACTER_MOVEMENT_TYPE::CHANGE_CHARACTER_MOVEMENT_TYPE_JUMP;
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (PrevMovementMode == EMovementMode::MOVE_Walking)
	{
		PlayerController->ChangeMoveMode(ChangeMovementType, true);
	}
	else if (PrevMovementMode == EMovementMode::MOVE_Falling)
	{
		PlayerController->ChangeMoveMode(ChangeMovementType, false);
		/*FVector ThisVelocity = PlayerCharacter->GetVelocity();
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("JumpJump OnMovementModeChanged.MOVE_Falling Velocity=(%f, %f, %f),   IsFalling==%d"), ThisVelocity.X, ThisVelocity.Y, ThisVelocity.Z, IsFalling ? 1 : 0);*/
		
		if (PlayerCharacter->GetBaseAnimInstance())
		{
			if (PlayerCharacter->IsActiveMoveing())
			{
				ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MLAND);
			}
			else
			{
				ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SLAND);
			}

			const FCHARACTER_MOVE_CACHE_DATA& CharacterMoveData = PlayerCharacter->GetCharacterMoveCacheData();
			PlayerCharacter->SetGravityScale(CharacterMoveData.GravityScale);///还原重力系数
		}
	}
}

void UJumpComponent::UpdateJumpState(JUMP_SHOW_STATE InJumpShowState)
{
	CurJumpShowState = InJumpShowState;
}

void UJumpComponent::OnStartLedgesJump(bool bUpJump, float JumpHeight)
{
	//如果障碍物高度大于一段跳高度，则不能执行辅助起跳,因为跳不上去
	if (JumpHeight <= ONE_JUMP_HEIGHT)
	{
		if (bUpJump)
		{
			LedgesJumpHeight = JumpHeight;
			OnStartActiveJump();
		}
		else
		{
			OnStartPassiveJump(JumpHeight);
		}
	}
}

void UJumpComponent::SetJumpShowType(JUMP_SHOW_TYPE InJumpShowType)
{
	//JumpShowType = InJumpShowType;
}

void UJumpComponent::SetJumpHeight(float JumpHeight)
{
	AGameCharacter* GameCharacter = Cast<AGameCharacter>(GetOwnerCharacter());
	if (IsValid(GameCharacter))
	{
		float GravityZ = -980.f * GameCharacter->GravityScaleBase;
		float JumpZVelocity = FMath::Sqrt((GravityZ * -2.0f) * JumpHeight);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("AGameCharacter::SetJumpZVelocity  [JumpHeight=%f]"), JumpZVelocity);
		GetOwnerCharacter()->GetCharacterMovement()->JumpZVelocity = JumpZVelocity;
	}
}

bool UJumpComponent::IsCanJump()
{
	if (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() <= EGameStatus::Teleport)
	{
		return false;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetOwnerCharacter());
	if (!IsValid(PlayerCharacter))
	{
		return false;
	}
	if (!PlayerCharacter->CanJump() || PlayerCharacter->JumpCurrentCount >= PlayerJumpMaxCount)
	{
		return false;
	}

	URoleStateInterface* RoleStateInst = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.StateInterface : nullptr);
	if (RoleStateInst && RoleStateInst->IsActionForbid(ACTION_FLAG::ACTION_FORBID_JUMP))
	{
		return false;
	}
	if (PlayerCharacter->GetCharacterMovement()->IsFlying() || 
		PlayerCharacter->GetCharacterMovement()->IsSwimming())
	{
		return false;
	}
	return true;
}

void UJumpComponent::SetSynchroPlayerJumpState(JUMP_SHOW_STATE InJumpShowState)
{
	CurJumpShowState = InJumpShowState;
	switch (CurJumpShowState)
	{
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_STAND:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_SLAND:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_MLAND:
		{
			IsJumpState = false;
			IsTheLand = true;
			IsTheUping = false;
			IsTheFalling = false;
			break;
		}
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_UP:
		{
			IsJumpState = true;
			IsTheLand = false;
			IsTheUping = true;
			IsTheFalling = false;
			break;
		}
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_DOWN:
		{
			IsJumpState = true;
			IsTheLand = false;
			IsTheUping = false;
			IsTheFalling = true;
			break;
		}
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_SJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_MJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_SJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_MJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_SJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_MJUMP:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_FLOAT:
		case JUMP_SHOW_STATE::JUMP_SHOW_STATE_PASSIVE:
		{
			IsJumpState = true;
			IsTheLand = false;
			IsTheUping = false;
			IsTheFalling = false;
			break;
		}
		default:
		{
			IsJumpState = false;
			IsTheLand = true;
			IsTheUping = false;
			IsTheFalling = false;
			break;
		}
	}
}

JUMP_SHOW_STATE UJumpComponent::GetCurJumpShowState()
{
	return CurJumpShowState;
}

void UJumpComponent::CheckJumpFalling()
{
	//检测是空中上升or下落状态
	FVector ActorLoction = GetOwner()->GetActorLocation();
	if (GetOwnerCharacter()->GetCharacterMovement()->IsFlying())
	{
		OldLoctionForJumpHorizontal = ActorLoction;
		return;
	}

	if (GetOwnerCharacter()->GetCharacterMovement()->IsFalling())
	{
		IsJumpState = true;
		IsTheLand = false;
	}

	if (!IsJumpState || IsTheLand)
	{
		IsTheFalling = false;
		IsTheUping = false;
		OldLoctionForJumpHorizontal = FVector(ActorLoction.X, ActorLoction.Y, ActorLoction.Z - 0.2f);
		ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_STAND);
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UJumpComponent::CheckJumpFalling11111111 (ThanValue=%f,  ActorLoction.Z=%f,   OldLoctionForJumpHorizontal.Z=%f)"),
			(ActorLoction.Z - OldLoctionForJumpHorizontal.Z), ActorLoction.Z, OldLoctionForJumpHorizontal.Z);
		if (!FMath::IsNearlyZero(OldLoctionForJumpHorizontal.Z))
		{
			if (ActorLoction.Z - OldLoctionForJumpHorizontal.Z > 0.1f)
			{
				IsTheUping = true;
				IsTheFalling = false;
				ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_UP);
			}
			else
			{
				IsTheUping = false;
				IsTheFalling = true;
				ChangeJumpStateToServer(JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_DOWN);
			}
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("UJumpComponent::CheckJumpFalling222222 (IsTheUping=%d,  IsTheFalling=%d)"),
				IsTheUping ? 1 : 0, IsTheFalling ? 1 : 0);
		}
		OldLoctionForJumpHorizontal = ActorLoction;
	}
}

ACharacter* UJumpComponent::GetOwnerCharacter()
{
	return Cast<ACharacter>(GetOwner());
}

CONTROL_COMPILE_OPTIMIZE_END

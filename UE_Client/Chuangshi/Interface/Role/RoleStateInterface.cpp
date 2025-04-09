// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleStateInterface.h"

#include "GameData/GameDeFine.h"

#include "Actor/Player/PlayerCharacter.h"
#include "Util/CS3Debug.h"
#include "StateMachine/RoleStateMachine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Component/Role/JumpComponent.h"
#include "Component/AvatarFilterActorComponent.h"


CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleStateInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleStateInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleStateInterface::URoleStateInterface()
{
}


void URoleStateInterface::OnStateChanged(const int32 & NewState, const int32 & OldState)
{
	UStateInterface::OnStateChanged(NewState, OldState);
	OnStateChangedBP(NewState, OldState);
/**
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (OffthewarTimer.IsValid())
	{
		ClearTimer(OffthewarTimer);
	}
	if (!IsValid(PlayerActor))return;
	if ((ENTITY_STATE)NewState == ENTITY_STATE::EntityStateFree && (ENTITY_STATE)OldState == ENTITY_STATE::EntityStateFight)
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(PlayerActor->GetController());
		CS3_MOVE_TYPE MoveType = PlayerController->GetMoveType();
		if (MoveType == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
		{
			if (!PlayerActor->IsCarrierState())
			{
				FString SpaceName = PlayerActor->GetNavigateNPCInfo().SpaceName;
				bool IsSearch = PlayerActor->GetNavigateNPCInfo().IsSearch;
				float NearbyRange = PlayerActor->GetNavigateNPCInfo().NearbyRange;
				int AutoQuestID = PlayerActor->GetNavigateNPCInfo().AutoQuestID;
				FVector DstPosition = PlayerActor->GetNavigateNPCInfo().DstPosition;
				PlayerActor->ActivateNavigateMoveModeOperation(true, DstPosition, NearbyRange, SpaceName, AutoQuestID, IsSearch, false);
				//PlayerActor->StartAutoNavigate(DstPosition, NearbyRange, SpaceName, AutoQuestID, IsSearch);

			}
		}
		else
		{
			if (!PlayerActor->IsCarrierState())
			{
				SetTimer(this, OffthewarTimer, FTimerDelegate::CreateLambda([this, PlayerActor]()
				{
					KBEngine::FVariantArray args;
					PlayerActor->GetSelfEntity()->CellCall(TEXT("transformPet"), args);
				}), 1.0f, false);
			}
		}
	}
*/
}

void URoleStateInterface::OnRep_state()
{
	UStateInterface::OnRep_state();

}

void URoleStateInterface::OnRepJumpState_Implementation(int32 JumpState)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null error:URoleStateInterface::OnRepJumpState : GetEntity()!"));
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步跳跃表现
	}

	///同步本地其他玩家的跳跃属性
	if (IsValid(PlayerCharacter->JumpComponent))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("===UBAnim::OnRepJumpState[1][EntityId=%d,  JumpShowType=%d"),
			GetEntity()->ID(), JumpState);

		PlayerCharacter->JumpComponent->SetSynchroPlayerJumpState((JUMP_SHOW_STATE)JumpState);

		//设置跳跃时平滑的时间
		UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(
			PlayerCharacter->GetFilterComponent());
		if (IsValid(Comp))
		{
			if (PlayerCharacter->JumpComponent->IsJumpState)
			{
				Comp->SetSmoothFilterLatencyFrames(0.1f);
			}
			else
			{
				Comp->SetSmoothFilterLatencyFrames(2.0f);
			}
		}
	}

	UpdateJumpState((JUMP_SHOW_STATE)JumpState);
}

void URoleStateInterface::UpdateJumpState(JUMP_SHOW_STATE JumpState)
{
	/*AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	int32 PlayerEntityId = PlayerActor->GetSelfEntity()->ID();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("URoleStateInterface::OnRepJumpState (EntityID=%d, JumpState=%d,  PlayerEntityId=%d)"),
		EntityID, (int32)JumpState, PlayerEntityId);*/
	if (RoleStateMachine)
	{
		RoleStateMachine->UpdateJumpState(JumpState);
	}
}

void URoleStateInterface::RequestChangeJumpState(JUMP_SHOW_STATE JumpState)
{
	if (nullptr != GetEntity())
	{
		KBEngine::FVariantArray args;
		args.Add((int32)JumpState);
		args.Add((uint8)0); 
		GetEntity()->CellCall(TEXT("ChangeRoleJumpState"), args);
	}
}

void URoleStateInterface::OnRep_climbLadderState()
{
	if (GetEntity() == nullptr)
	{
		return;
	}
	int32 ClimbLadderState = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("climbLadderState"));
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===URoleStateInterface::OnRepClimbLadderState[1][EntityId=%d,  ClimbLadderState=%d"),
		GetEntity()->ID(), ClimbLadderState);

	PlayerCharacter->LadderCustomMovmentCpt->SetSynchroPlayerClimbLadderState((CLIMB_LADDER_STATE)ClimbLadderState);
	if (RoleStateMachine)
	{
		RoleStateMachine->UpdateClimbLadderState((CLIMB_LADDER_STATE)ClimbLadderState);
	}

	//设置攀爬时平滑的时间
	UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(
		PlayerCharacter->GetFilterComponent());
	if (IsValid(Comp))
	{
		if (PlayerCharacter->LadderCustomMovmentCpt->IsLadderMovement())
		{
			Comp->SetSmoothFilterLatencyFrames(0.1f);
		}
		else
		{
			Comp->SetSmoothFilterLatencyFrames(2.0f);
		}
	}
}

void URoleStateInterface::RequestChangeClimbLadderState(CLIMB_LADDER_STATE ClimbLadderState)
{
	if (nullptr != GetEntity())
	{
		KBEngine::FVariantArray args;
		args.Add((int32)ClimbLadderState);
		GetEntity()->CellCall(TEXT("ChangeClimbLadderState"), args);
	}
}

void URoleStateInterface::OnRep_ladderPosOffset()
{
	if (GetEntity() == nullptr)
	{
		return;
	}
	float SynchroClimbLadderActionFramePos = UGolbalBPFunctionLibrary::GetFloatPropertyValue(GetEntity()->ID(), TEXT("ladderPosOffset"));
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("===URoleStateInterface::OnRepClimbLadderState[2][EntityId=%d,  LadderPosOffset=%f"),
		PlayerCharacter->GetSelfEntity()->ID(), SynchroClimbLadderActionFramePos);
	
	if (PlayerCharacter->LadderCustomMovmentCpt)
	{
		PlayerCharacter->LadderCustomMovmentCpt->ClimbLadderActionFramePos = SynchroClimbLadderActionFramePos;
	}
}

void URoleStateInterface::RequestUpdateClimbLadderActionStepPos(float LadderPosOffset)
{
	if (nullptr != GetEntity())
	{
		KBEngine::FVariantArray args;
		args.Add(LadderPosOffset);
		GetEntity()->CellCall(TEXT("UpdateClimbLadderActionStepPos"), args);
	}
}

void URoleStateInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnStateChangedBP");
	ArrBlueFunc.Add("OnRep_state");
	ArrBlueFunc.Add("OnRepJumpState");
	Supper::InitBlueCB();
}

CONTROL_COMPILE_OPTIMIZE_END

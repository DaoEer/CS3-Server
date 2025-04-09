
#include "RoleStateMachine.h"
//CS3Êý¾Ý
#include "GameData/StateData.h"
#include "GameData/GameDeFine.h"
//CS3
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "EffectState/EffectStateDizzy.h"
#include "EffectState/EffectStateUnControllable.h"
#include "EffectState/EffectStateInvincible.h"
#include "EffectState/EffectStateHitBack.h"
#include "EffectState/EffectStateFix.h"
#include "EffectState/EffectStateSleep.h"
#include "EffectState/EffectStateWind.h"
#include "EffectState/EffectStateProtect.h"
#include "EffectState/EffectStateConfusion.h"
#include "EffectState/EffectStateHide.h"
#include "JumpState/JumpBaseState.h"
#include "JumpState/JumpStandState.h"
#include "JumpState/JumpMoveUpState.h"
#include "JumpState/JumpStandUpState.h"
#include "JumpState/JumpTwoStandUpState.h"
#include "JumpState/JumpTwoMoveUpState.h"
#include "JumpState/JumpThreeMoveUpState.h"
#include "JumpState/JumpStandLandState.h"
#include "JumpState/JumpMoveLandState.h"
#include "JumpState/JumpThreeStandUpState.h"
#include "JumpState/JumpAirUpState.h"
#include "JumpState/JumpAirDownState.h"
#include "JumpState/JumpFloatState.h"
#include "JumpState/JumpPassiveState.h"
#include "ClimbLadderState/ClimbLadderBaseState.h"
#include "ClimbLadderState/ClimbLadderEnterZoneState.h"
#include "ClimbLadderState/ClimbLadderEnterBottomState.h"
#include "ClimbLadderState/ClimbLadderExitBottom.h"
#include "ClimbLadderState/ClimbLadderExitTopState.h"
#include "ClimbLadderState/ClimbLadderMoveState.h"
#include "ClimbLadderState/ClimbLadderFallExitLandState.h"
#include "ClimbLadderState/ClimbLadderFallExitState.h"
#include "ClimbLadderState/ClimbLadderStandState.h"
#include "EffectState/EffectStateFreeze.h"
#include "Actor/Player/PlayerCharacter.h"


CONTROL_COMPILE_OPTIMIZE_START
TMap<EFFECT_STATE, TSharedPtr<EffectStateBase>> URoleStateMachine::EffectStateMap;

void URoleStateMachine::InitStateMap(KBEngine::Entity* RoleEntity)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_STATE);
	TArray<FName> StateRowNameList = ConfigTable->GetRowNames();
	for (FName RowName : StateRowNameList)
	{
		const FSTATE_DATA* TableData = ConfigTable->GetRow<FSTATE_DATA>(RowName.ToString());
		checkf(TableData->StateClass != UBaseState::StaticClass(), TEXT("-------RowName = %s Class Type Error!-------"));
		UBaseState* StateClass = NewObject<UBaseState>(this, TableData->StateClass);
		StateClass->CreateState(TableData, this, RoleEntity);
		RoleStateMap.Add(TableData->State, StateClass);
	}
	CurrentEntity = RoleEntity;
	//CurrentState = RoleStateMap[ENTITY_STATE::EntityStateFree];
}

void URoleStateMachine::InitEffectStateMap()
{
	if (URoleStateMachine::EffectStateMap.Num()==0)
	{
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_DIZZY, TSharedPtr<EffectStateBase>(new EffectStateDizzy()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_UNCONTROLLABLE, TSharedPtr<EffectStateBase>(new EffectStateUnControllable()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_INVINCIBLE, TSharedPtr<EffectStateBase>(new EffectStateInvincible()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_HIT_BACK, TSharedPtr<EffectStateBase>(new EffectStateHitBack()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_FIX, TSharedPtr<EffectStateBase>(new EffectStateFix()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_SLEEP, TSharedPtr<EffectStateBase>(new EffectStateSleep()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_WIND, TSharedPtr<EffectStateBase>(new EffectStateWind()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_CONFUSION, TSharedPtr<EffectStateBase>(new EffectStateConfusion()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_HIDE, TSharedPtr<EffectStateBase>(new EffectStateHide()));
		URoleStateMachine::EffectStateMap.Add(EFFECT_STATE::EFFECT_STATE_FREEZE, TSharedPtr<EffectStateBase>(new EffectStateFreeze()));
	}
}

void URoleStateMachine::InitJumpStateMap()
{
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_STAND, TSharedPtr<JumpBaseState>(new JumpStandState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SJUMP, TSharedPtr<JumpBaseState>(new JumpStandUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MJUMP, TSharedPtr<JumpBaseState>(new JumpMoveUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_SJUMP, TSharedPtr<JumpBaseState>(new JumpTwoStandUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_MJUMP, TSharedPtr<JumpBaseState>(new JumpTwoMoveUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_SJUMP, TSharedPtr<JumpBaseState>(new JumpThreeStandUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_MJUMP, TSharedPtr<JumpBaseState>(new JumpThreeMoveUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_UP, TSharedPtr<JumpBaseState>(new JumpAirUpState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_DOWN, TSharedPtr<JumpBaseState>(new JumpAirDownState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SLAND, TSharedPtr<JumpBaseState>(new JumpStandLandState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MLAND, TSharedPtr<JumpBaseState>(new JumpMoveLandState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_FLOAT, TSharedPtr<JumpBaseState>(new JumpFloatState()));
	RoleJumpStateMap.Add(JUMP_SHOW_STATE::JUMP_SHOW_STATE_PASSIVE, TSharedPtr<JumpBaseState>(new JumpPassiveState()));

	for (auto Object : RoleJumpStateMap)
	{
		TSharedPtr<JumpBaseState> FindJumpBaseState = Object.Value;
		FindJumpBaseState->CreateState(this, CurrentEntity);
	}
}

void URoleStateMachine::InitClimbLadderStateMap()
{
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_STAND, TSharedPtr<ClimbLadderStandState>(new ClimbLadderStandState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_ENTER_ZONE, TSharedPtr<ClimbLadderEnterZoneState>(new ClimbLadderEnterZoneState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_ENTER_BOTTOM, TSharedPtr<ClimbLadderEnterBottomState>(new ClimbLadderEnterBottomState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_EXIT_BOTTOM, TSharedPtr<ClimbLadderExitBottom>(new ClimbLadderExitBottom()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_EXIT_TOP, TSharedPtr<ClimbLadderExitTopState>(new ClimbLadderExitTopState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_MOVE, TSharedPtr<ClimbLadderMoveState>(new ClimbLadderMoveState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_FALL_EXIT, TSharedPtr<ClimbLadderFallExitState>(new ClimbLadderFallExitState()));
	ClimbLadderStateMap.Add(CLIMB_LADDER_STATE::CLIMB_LADDER_STATE_FALL_EXIT_LAND, TSharedPtr<ClimbLadderFallExitLandState>(new ClimbLadderFallExitLandState()));

	for (auto Object : ClimbLadderStateMap)
	{
		TSharedPtr<ClimbLadderBaseState> FindClimbLadderBaseState = Object.Value;
		FindClimbLadderBaseState->CreateState(this, CurrentEntity);
	}
}

void URoleStateMachine::UpdateState(ENTITY_STATE NewState)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("URoleStateMachine::UpdateState[EntityId = %d, NewState:%d]"), CurrentEntity->ID(), (int32)NewState);
	RoleState = StateTransition(NewState);
	if (RoleState)
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
		if (CurrentState)
		{
			CurrentState->Exit();
		}

		if (IsValid(PlayerCharacter))
		{
			ENTITY_STATE CurState = CurrentState ? CurrentState->GetRoleState() : ENTITY_STATE::EntityStateMax;
			PlayerCharacter->CheckChangeState(NewState, CurState);
		}

		CurrentState = RoleState;
		CurrentState->Enter();
	}
}

void URoleStateMachine::OnAddEffectState(EFFECT_STATE EffectState_)
{
	if (EffectStateMap.Contains(EffectState_))
	{
		TSharedPtr<EffectStateBase> EffectState = EffectStateMap[EffectState_];
		EffectStateMap[EffectState_]->Add(CurrentEntity->Actor());
	}
}

void URoleStateMachine::OnDelEffectState(EFFECT_STATE EffectState_)
{
	if (EffectStateMap.Contains(EffectState_))
	{
		TSharedPtr<EffectStateBase> EffectState = EffectStateMap[EffectState_];
		EffectState->Del(CurrentEntity->Actor());
	}
}

void URoleStateMachine::UpdateJumpState(JUMP_SHOW_STATE JumpShowState)
{
	if (RoleJumpStateMap.Contains(JumpShowState))
	{
		TSharedPtr<JumpBaseState> FindJumpBaseState = RoleJumpStateMap[JumpShowState];
		FindJumpBaseState->Enter();
	}
}

void URoleStateMachine::UpdateClimbLadderState(CLIMB_LADDER_STATE ClimbLadderState)
{
	if (ClimbLadderStateMap.Contains(ClimbLadderState))
	{
		TSharedPtr<ClimbLadderBaseState> FindClimbLadderBaseState = ClimbLadderStateMap[ClimbLadderState];
		FindClimbLadderBaseState->Enter();
	}
}

UBaseState* URoleStateMachine::StateTransition(ENTITY_STATE State)
{
	if (RoleStateMap.Contains(State))
	{
		RoleState = RoleStateMap[State];
	}
	return RoleState;
}

void URoleStateMachine::OnActionCallBack(ACharacter *RoleChar, FName id)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("========URoleStateMachine::OnActionCallBack  callBack(), id=%s"), *(id.ToString()));
	if (CurrentState)
	{
		CurrentState->Exit();
	}
	CurrentState = RoleState;
	CurrentState->Enter();
}
CONTROL_COMPILE_OPTIMIZE_END


#include "BaseState.h"
//CS3Êı¾İ
#include "GameData/GameDeFine.h"
//CS3
#include "RoleStateMachine.h"

void UBaseState::CreateState(const FSTATE_DATA* TableData, URoleStateMachine* StateMachine, KBEngine::Entity* RoleEntity)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------UBaseState::CreateState-->>EntityId = %d---------------"), RoleEntity->ID());
	StateTableData = TableData;
	CurrentEntity = RoleEntity; 
	CurrentStateMachine = StateMachine;
}

void UBaseState::Enter()
{

}

void UBaseState::Execute()
{

}

void UBaseState::Exit()
{
	
}

ENTITY_STATE UBaseState::GetRoleState()
{
	return StateTableData->State;
}

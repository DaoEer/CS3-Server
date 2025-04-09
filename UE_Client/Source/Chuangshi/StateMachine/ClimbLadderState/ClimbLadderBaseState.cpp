#include "ClimbLadderBaseState.h"
//CS3Êý¾Ý
#include "GameData/GameDeFine.h"
#include "Entity.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
//CS3

void ClimbLadderBaseState::CreateState(URoleStateMachine* StateMachine, KBEngine::Entity* RoleEntity)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------UClimbLadderBaseState::CreateState-->>EntityId = %d---------------"), RoleEntity->ID());
	CurrentEntity = RoleEntity; 
	CurrentStateMachine = StateMachine;
}

ClimbLadderBaseState::ClimbLadderBaseState()
{

}

ClimbLadderBaseState::~ClimbLadderBaseState()
{

}

void ClimbLadderBaseState::Enter()
{

}

void ClimbLadderBaseState::Exit()
{
	
}

void ClimbLadderBaseState::PlayJumpAction(const int32& ContinuousId, 
	const TArray<FString>& JumpActionID, const TArray<FString>& BeginTime)
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter)
	{
	}
}


#include "JumpFloatState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpFloatState::JumpFloatState()
{

}

JumpFloatState::~JumpFloatState()
{

}

void JumpFloatState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_FLOAT);
	}
}

void JumpFloatState::Exit()
{
}

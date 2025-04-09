#include "JumpMoveUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpMoveUpState::JumpMoveUpState()
{

}

JumpMoveUpState::~JumpMoveUpState()
{

}

void JumpMoveUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MJUMP);

		FName ActionId = "JumpStart_Move";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpMoveUpState::Exit()
{
}

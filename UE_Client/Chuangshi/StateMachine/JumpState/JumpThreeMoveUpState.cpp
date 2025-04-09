#include "JumpThreeMoveUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpThreeMoveUpState::JumpThreeMoveUpState()
{

}

JumpThreeMoveUpState::~JumpThreeMoveUpState()
{

}

void JumpThreeMoveUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_MJUMP);

		FName ActionId = "JumpStart_Step3";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpThreeMoveUpState::Exit()
{
}

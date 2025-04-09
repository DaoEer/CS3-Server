#include "JumpStandUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpStandUpState::JumpStandUpState()
{

}

JumpStandUpState::~JumpStandUpState()
{

}

void JumpStandUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SJUMP);

		FName ActionId = "JumpStart_Stand";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpStandUpState::Exit()
{
}

#include "JumpTwoStandUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpTwoStandUpState::JumpTwoStandUpState()
{

}

JumpTwoStandUpState::~JumpTwoStandUpState()
{

}

void JumpTwoStandUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_TWO_SJUMP);

		FName ActionId = "JumpStart_Step2";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpTwoStandUpState::Exit()
{
}

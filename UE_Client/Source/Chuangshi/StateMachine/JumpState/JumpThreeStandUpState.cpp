#include "JumpThreeStandUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpThreeStandUpState::JumpThreeStandUpState()
{

}

JumpThreeStandUpState::~JumpThreeStandUpState()
{

}

void JumpThreeStandUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_THREE_SJUMP);

		FName ActionId = "JumpStart_Step3";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpThreeStandUpState::Exit()
{
}

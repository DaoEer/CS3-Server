#include "JumpMoveLandState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpMoveLandState::JumpMoveLandState()
{

}

JumpMoveLandState::~JumpMoveLandState()
{

}

void JumpMoveLandState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_MLAND);

		FName ActionId = "JumpEnd_Move";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpMoveLandState::Exit()
{
}

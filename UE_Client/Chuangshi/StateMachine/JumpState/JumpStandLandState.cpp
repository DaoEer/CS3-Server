#include "JumpStandLandState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpStandLandState::JumpStandLandState()
{

}

JumpStandLandState::~JumpStandLandState()
{

}

void JumpStandLandState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_SLAND);

		FName ActionId = "JumpEnd_Stand";
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpStandLandState::Exit()
{
}

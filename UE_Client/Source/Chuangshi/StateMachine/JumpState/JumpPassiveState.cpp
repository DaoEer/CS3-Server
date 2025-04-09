
#include "JumpPassiveState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

JumpPassiveState::JumpPassiveState()
{

}

JumpPassiveState::~JumpPassiveState()
{

}

void JumpPassiveState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpCurrentCount--;
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_PASSIVE);

		FName ActionId = "JumpStart_Passive1"; 
		CurrentPlayerCharacter->PlayAction(ActionId);
	}
}

void JumpPassiveState::Exit()
{
}

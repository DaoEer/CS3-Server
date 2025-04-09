
#include "ClimbLadderExitTopState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"
#include "GameData/CharacterData.h"
#include "GameFramework/Character.h"
#include "Actor/Action/BaseAnimInstance.h"

ClimbLadderExitTopState::ClimbLadderExitTopState()
{

}

ClimbLadderExitTopState::~ClimbLadderExitTopState()
{

}

void ClimbLadderExitTopState::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_ROOT_MOTION;

		FName ActionId = "LadderExitTop";
		PlayerCharacter->PlayAction(ActionId);
	}
}

void ClimbLadderExitTopState::Exit()
{
}


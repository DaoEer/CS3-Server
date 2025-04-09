
#include "ClimbLadderFallExitLandState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

ClimbLadderFallExitLandState::ClimbLadderFallExitLandState()
{

}

ClimbLadderFallExitLandState::~ClimbLadderFallExitLandState()
{

}

void ClimbLadderFallExitLandState::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_NONE;

		if (IsValid(PlayerCharacter->GetBaseAnimInstance()))
		{
			PlayerCharacter->GetBaseAnimInstance()->PlayFallLandAction();
		}
	}
}

void ClimbLadderFallExitLandState::Exit()
{
}

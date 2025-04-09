
#include "ClimbLadderFallExitState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

ClimbLadderFallExitState::ClimbLadderFallExitState()
{

}

ClimbLadderFallExitState::~ClimbLadderFallExitState()
{

}

void ClimbLadderFallExitState::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Falling);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_NONE;

		if (IsValid(PlayerCharacter->GetBaseAnimInstance()))
		{
			PlayerCharacter->GetBaseAnimInstance()->StopAction();
			PlayerCharacter->GetBaseAnimInstance()->PlayFallingAction();
		}
	}
}

void ClimbLadderFallExitState::Exit()
{
}

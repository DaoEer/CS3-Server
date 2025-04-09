
#include "ClimbLadderStandState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

ClimbLadderStandState::ClimbLadderStandState()
{

}

ClimbLadderStandState::~ClimbLadderStandState()
{

}

void ClimbLadderStandState::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_NONE;
		if (IsValid(PlayerCharacter->GetBaseAnimInstance()))
		{
			PlayerCharacter->GetBaseAnimInstance()->StopAction();
		}
	}
}

void ClimbLadderStandState::Exit()
{
}

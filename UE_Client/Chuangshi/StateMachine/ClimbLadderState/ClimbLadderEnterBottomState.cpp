
#include "ClimbLadderEnterBottomState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"
#include "GameData/CharacterData.h"
#include "GameFramework/Character.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/Role/LadderCustomMovementComponent.h"

ClimbLadderEnterBottomState::ClimbLadderEnterBottomState()
{

}

ClimbLadderEnterBottomState::~ClimbLadderEnterBottomState()
{

}

void ClimbLadderEnterBottomState::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Custom, (uint8)CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_ROOT_MOTION);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_ROOT_MOTION;
		PlayerCharacter->LadderCustomMovmentCpt->IsRootMotionHaveUpAction = true;

		FName LadderEnterBottom = "LadderEnterBottom";
		PlayerCharacter->PlayAction(LadderEnterBottom);
	}
}

void ClimbLadderEnterBottomState::Exit()
{
}


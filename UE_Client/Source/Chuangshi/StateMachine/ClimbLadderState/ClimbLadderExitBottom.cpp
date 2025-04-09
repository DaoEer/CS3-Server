
#include "ClimbLadderExitBottom.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"
#include "GameFramework/Character.h"
#include "Actor/Action/BaseAnimInstance.h"

ClimbLadderExitBottom::ClimbLadderExitBottom()
{

}

ClimbLadderExitBottom::~ClimbLadderExitBottom()
{

}

void ClimbLadderExitBottom::Enter()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(PlayerCharacter) && IsValid(PlayerCharacter->LadderCustomMovmentCpt))
	{
		PlayerCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		PlayerCharacter->LadderCustomMovmentCpt->TempCustomMovementMode = CUSTOM_MOVEMENT_MODE_ENUM::CUSTOM_MOVEMENT_ROOT_MOTION;

		FName LadderEnterBottom = "LadderExitBottom";
		PlayerCharacter->PlayAction(LadderEnterBottom);
	}
}

void ClimbLadderExitBottom::Exit()
{
}
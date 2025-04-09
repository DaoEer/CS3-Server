
#include "ClimbLadderEnterZoneState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "GameData/GameDeFine.h"

ClimbLadderEnterZoneState::ClimbLadderEnterZoneState()
{

}

ClimbLadderEnterZoneState::~ClimbLadderEnterZoneState()
{

}

void ClimbLadderEnterZoneState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (IsValid(CurrentPlayerCharacter))
	{
		
	}
}

void ClimbLadderEnterZoneState::Exit()
{
}

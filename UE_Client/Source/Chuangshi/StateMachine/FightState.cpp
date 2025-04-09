
#include "FightState.h"
#include "RoleStateMachine.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
void UFightState::Enter()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnEnterFightState();
	}
}

void UFightState::Execute()
{

}

void UFightState::Exit()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnExitFightState();
	}
}

CONTROL_COMPILE_OPTIMIZE_END

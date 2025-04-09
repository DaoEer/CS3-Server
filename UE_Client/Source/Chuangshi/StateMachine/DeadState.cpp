
#include "DeadState.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
void UDeadState::Enter()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UDeadState::Enter[Entityid = %d,  CurrentActor=%d]"), CurrentEntity->ID(), CurrentActor ? 1:0);
	if (CurrentActor)
	{
		CurrentActor->OnEnterDeadState();
	}
}

void UDeadState::Execute()
{

}

void UDeadState::Exit()
{
	AServerCharacter* CurrentActor = Cast<AServerCharacter>(CurrentEntity->Actor());
	if (CurrentActor)
	{
		CurrentActor->OnExitDeadState();
	}
}

CONTROL_COMPILE_OPTIMIZE_END

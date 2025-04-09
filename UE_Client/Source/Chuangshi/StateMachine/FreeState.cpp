
#include "FreeState.h"
#include "RoleStateMachine.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

void UFreeState::Enter()
{
	if (CurrentEntity)
	{
		AServerCharacter* ServerCharacter = (AServerCharacter*)CurrentEntity->Actor();
		if (ServerCharacter)
		{
			ServerCharacter->OnEnterFreeState();
			//ServerCharacter->PlayActionToType(ACTION_TYPE_ENUM::ACTION_TYPE_STANDBY);
		}
	}
}

void UFreeState::Execute()
{

}

void UFreeState::Exit()
{
	
}

CONTROL_COMPILE_OPTIMIZE_END

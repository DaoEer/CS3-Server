#include "JumpBaseState.h"
//CS3Êý¾Ý
#include "GameData/GameDeFine.h"
#include "Entity.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
//CS3

void JumpBaseState::CreateState(URoleStateMachine* StateMachine, KBEngine::Entity* RoleEntity)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------UJumpBaseState::CreateState-->>EntityId = %d---------------"), RoleEntity->ID());
	CurrentEntity = RoleEntity; 
	CurrentStateMachine = StateMachine;
}

JumpBaseState::JumpBaseState()
{

}

JumpBaseState::~JumpBaseState()
{

}

void JumpBaseState::Enter()
{

}

void JumpBaseState::Exit()
{
	
}

void JumpBaseState::PlayJumpAction(const int32& ContinuousId, 
	const TArray<FString>& JumpActionID, const TArray<FString>& BeginTime)
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter)
	{
		TArray<float> ActionStartTimes;
		TArray<FName> ActionIds;
		for (int i = 0; i < JumpActionID.Num(); i++)
		{
			FString ActionId = JumpActionID[i];
			if (!ActionId.IsEmpty())
			{
				//CS3_Display(CS3DebugType::CL_Undefined, TEXT("other ========%s"), *ActionId);
				ActionIds.Add(FSTRING_TO_FNAME(ActionId));
				ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
			}

			CS3_Display(CS3DebugType::CL_Undefined, TEXT("USkillInterface::OnNotifyJumpActions(EntityID=%d, ContinuousId=%d, ActionId=%s,  BeginTime=%s)"),
				CurrentEntity->ID(), ContinuousId, *ActionId, *(BeginTime[i]));
		}
		if (ActionIds.Num())
		{
			CurrentPlayerCharacter->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
		}
	}
}

// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Dec_CheckEntityState.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "Interface/StateInterface.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "AIController.h"

bool UMAI_Dec_CheckEntityState::EntityIsState(UBehaviorTreeComponent& OwnerComp, ENTITY_STATE state) const
{
	AMonsterCharacter* m = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(m))
	{
		return false;
	}

	if (m->GetSelfEntity() == nullptr)
	{
		return false;
	}

	CMonster* e = static_cast<CMonster*>(m->GetSelfEntity());
	if (!e)
	{
		return false;
	}
	else
	{
		UStateInterface* StateIns = m->GetEntityInterface_Cache().StateInterface;
		if (!IsValid(StateIns))
		{
			return false;
		}
		if (ENTITY_STATE( StateIns->CurrentState ) != state )
		{
			return false;
		}
	}

	return true;
}
// Fill out your copyright notice in the Description page of Project Settings.
#include "MAI_Dec_IsCanStart.h"

#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"



bool UMAI_Dec_IsCanStart::CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const
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

	CMonster* e = static_cast< CMonster* >( m->GetSelfEntity() );
	if (!e || e->IsControlled() == false)
	{
		return false;
	}

	return true;
}
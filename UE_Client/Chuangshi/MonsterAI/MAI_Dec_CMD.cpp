// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Dec_CMD.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "KBEngine.h"
#include "MonsterAI/MonsterAIEnum.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "AIController.h"


bool UMAI_Dec_CMD::CheckCMD(UBehaviorTreeComponent& OwnerComp, MONSTER_AI_COMMAND cmd) const
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
	if (e->GetControlCmd() == cmd && !e->IsExeCmd())
	{
		return true;
	}

	return false;
}

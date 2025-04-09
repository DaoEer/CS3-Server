// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_CMD.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "AIController.h"


EBTNodeResult::Type UMAI_Task_CMD::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	if (ExecuteCMD(OwnerComp) ==  MONSTER_AI_COMMAND_PROCESS::OVER )
	{
		OverCMD(OwnerComp);
	}
	return EBTNodeResult::Succeeded;
}

MONSTER_AI_COMMAND_PROCESS UMAI_Task_CMD::ExecuteCMD(UBehaviorTreeComponent& OwnerComp)
{
	return  MONSTER_AI_COMMAND_PROCESS::READY ;
}

void UMAI_Task_CMD::OverCMD(UBehaviorTreeComponent& OwnerComp)
{
	AMonsterCharacter* m = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(m))
	{
		return;
	}

	if (m->GetSelfEntity() == nullptr)
	{
		return;
	}

	CMonster* e = static_cast<CMonster*>(m->GetSelfEntity());

	e->OverExeCmd();

}



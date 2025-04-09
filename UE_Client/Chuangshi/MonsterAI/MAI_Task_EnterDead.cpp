// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_EnterDead.h"
#include "Util/CS3Debug.h"
#include "Actor/Monster/MonsterCharacter.h"

EBTNodeResult::Type UMAI_Task_EnterDead::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	actor->GetMovementComponent()->StopMovementImmediately();
	return EBTNodeResult::Succeeded;
}
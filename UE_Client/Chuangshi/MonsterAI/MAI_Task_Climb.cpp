// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_Climb.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDefault.h"
#include "GameData/GameDeFine.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/CS3Entity.h"
#include "Entity/Monster/CMonster.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Util/CS3Debug.h"
#include "MonsterAI/MonsterAIController.h"


EBTNodeResult::Type UMAI_Task_Climb::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	//1.搜寻最近的一个梯子，并且梯子的位置不处于自身下方
	//2.移动至梯子位置

	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(MonsterCharacter))
	{
		return EBTNodeResult::Failed;
	}
	CMonster* entity = static_cast<CMonster*>(MonsterCharacter->GetSelfEntity());
	if (!entity)
	{
		return EBTNodeResult::Failed;
	}

	TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("MonsterExtAerialLadder", 5000.f, MonsterCharacter->GetActorLocation());

	for (int i = 0; i < TempList.Num() - 1; i++)
	{
		for (int j = i + 1; j <= TempList.Num() - 1; j++)
		{

			if (FVector::Dist2D(TempList[i]->LocalPosition(), entity->LocalPosition()) < FVector::Dist2D(TempList[j]->LocalPosition(), entity->LocalPosition()))
			{
				CS3Entity* tempPtr = TempList[j];
				TempList[j] = TempList[i];
				TempList[i] = tempPtr;
			}
		}
	}
	bool FindTarget = false;
	FVector targetPos = FVector::ZeroVector;
	while (TempList.Num())
	{
		CS3Entity* target = TempList.Pop();
		if (entity->LocalPosition().Z - target->LocalPosition().Z <= 500.f)
		{
			targetPos = target->LocalPosition();
			break;
		}
	}

	if (!targetPos.IsZero())
	{
		AMonsterAIController* controller = Cast< AMonsterAIController >(MonsterCharacter->GetController());
		if (IsValid(controller))
		{
			controller->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::NONE));
			controller->MoveToPos(targetPos);
		}
	}


	return EBTNodeResult::Succeeded;


}
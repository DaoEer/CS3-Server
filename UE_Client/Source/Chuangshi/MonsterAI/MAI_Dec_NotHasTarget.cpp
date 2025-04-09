// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Dec_NotHasTarget.h"
#include "MonsterAI/MAI_Public_func.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDefault.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "AIController.h"

bool UMAI_Dec_NotHasTarget::CalculateRawConditionValue(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory) const
{
	int32 attackID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
	if (attackID == 0)
	{
		return true;
	}
	CS3Entity* attackEntity = GetCS3Entity(attackID);
	if (attackEntity == nullptr)
	{
		return true;
	}
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	CMonster* entity = static_cast<CMonster*>(actor->GetSelfEntity());

	if (entity->QueryRelation(attackEntity) != COMBAT_RELATION::COMBAT_RELATION_ENEMY) //有效攻击对象
	{
		return true;
	}
	return false;

}
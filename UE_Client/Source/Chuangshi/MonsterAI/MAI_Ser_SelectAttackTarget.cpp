// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_SelectAttackTarget.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDefault.h"
#include "CS3Base/CS3Entity.h"
#include "Interface/CombatInterface.h"
#include "MAI_Public_func.h"
#include "AIController.h"
#include "BehaviorTree/BlackboardComponent.h"

void UMAI_Ser_SelectAttackTarget::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	Super::TickNode(OwnerComp, NodeMemory, DeltaSeconds);

	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	CMonster* ownerEntity = static_cast<CMonster*>( actor->GetSelfEntity());
	if (!ownerEntity)
	{
		return;
	}

	UCombatInterface* cIntf = Cast< UCombatInterface >( ownerEntity->GetInterfaceByName( TEXT( "CombatInterface" ) ) );
	TMap<int32, int32> damageList = cIntf->GetDamageList();
	if (damageList.Num() > 0)
	{
		damageList.ValueSort([](const int32& IntegralA, const int32& IntegralB) {return IntegralA > IntegralB; });
		for (auto it = damageList.CreateConstIterator(); it; ++it)
		{
			KBEngine::Entity* e = GetEntity(it.Key());
			if (e != nullptr && ownerEntity->QueryRelation(e) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				//OwnerComp.GetBlackboardComponent()->SetValueAsInt(FName("AttackEntityID"), e->ID());
				return;
			}
		}
	}
	else
	{
		TMap<int32, int32> enemyList = cIntf->GetEnemyList();
		enemyList.ValueSort([](const int32& IntegralA, const int32& IntegralB) {return IntegralA > IntegralB; });
		for (auto it = enemyList.CreateConstIterator(); it; ++it)
		{
			KBEngine::Entity* e = GetEntity(it.Key());
			if (e != nullptr && ownerEntity->QueryRelation(e) == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				OwnerComp.GetBlackboardComponent()->SetValueAsInt(FName("AttackEntityID"), e->ID());
				return;
			}
		}
	}
	
}
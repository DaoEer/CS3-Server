// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_SearchEnemy.h"

#include "Actor/Monster/MonsterCharacter.h"
#include "Entity/Monster/CMonster.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDeFine.h"
#include "CS3Base/CS3Entity.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "CS3Base/GameObject.h"
#include "AIController.h"
#include "Interface/GameObjectInterface.h"

DECLARE_CYCLE_STAT(TEXT("CS3_AISearchEnemy_TickNode"), STAT_CS3_AISearchEnemy_TickNode, STATGROUP_CS3_AISearchEnemy);

void UMAI_Ser_SearchEnemy::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	SCOPE_CYCLE_COUNTER(STAT_CS3_AISearchEnemy_TickNode);
	
	Super::TickNode(OwnerComp, NodeMemory, DeltaSeconds);
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	CMonster* entity= static_cast<CMonster*>( actor->GetSelfEntity() );
	if (entity == nullptr)
	{
		return;
	}

	////取出现有的攻击对象ID
	//int32 attackID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
	//CS3Entity* attackEntity = static_cast<CS3Entity*>( UGolbalBPFunctionLibrary::FindEntity(attackID) );

	//if (attackEntity != nullptr && entity->QueryRelation(attackEntity) == COMBAT_RELATION::COMBAT_RELATION_ENEMY) //有效攻击对象
	//{
	//	return;
	//}


	//搜索敌对目标
	float SearchRange = OwnerComp.GetBlackboardComponent()->GetValueAsFloat(FName("SearchRange"));

	TArray<ENTITY_TYPE> enemyTypes;
	enemyTypes.Add(ENTITY_TYPE::ENTITY_FLAG_MONSTER);
	enemyTypes.Add(ENTITY_TYPE::ENTITY_FLAG_ROLE);
	enemyTypes.Add(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET);
	bool FindTarget = false;
	
	//是否是远程兵
	bool IsRemote = OwnerComp.GetBlackboardComponent()->GetValueAsBool(FName("IsRemote"));
	int32 AttackEntityID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
	if (IsRemote == true)
	{
		if (AttackEntityID != 0)
		{
			GameObject* AttackEntity = static_cast<GameObject*>(UGolbalBPFunctionLibrary::FindEntity(AttackEntityID));
			if (AttackEntity != nullptr && !AttackEntity->IsState(ENTITY_STATE::EntityStateDead) && FVector::Dist2D(entity->LocalPosition(), AttackEntity->LocalPosition()) <= SearchRange)
			{
				return;
			}
		}
		TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", SearchRange, actor->GetActorLocation());
		//远程兵随机选择敌人
		TArray<CS3Entity*> EnemyList = TempList.FilterByPredicate([&enemyTypes, &entity](CS3Entity* TempEntity)
			{
				GameObject* TargetEntity = static_cast<GameObject*>(TempEntity);
				UGameObjectInterface* TargetInterface = TargetEntity->Interface_Cache.GameObjectInterface;

				if (TargetEntity->IsState(ENTITY_STATE::EntityStateDead) || !enemyTypes.Contains(TargetInterface->getEntityFlag()))
				{
					return false;
				}
				if (TargetEntity->ID() == entity->ID())
				{
					return false;
				}
				COMBAT_RELATION relation = entity->QueryRelation(TargetEntity);
				if (relation == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
				{
					return true;
				}
				return false;
			});
		if (EnemyList.Num() > 0)
		{
			int32 Index = FMath::RandRange(0, EnemyList.Num() - 1);
			GameObject* TargetEntity = static_cast<GameObject*>(EnemyList[Index]);
			KBEngine::FVariantArray args;
			args.Add(TargetEntity->ID());
			entity->CellCall(TEXT("CAI_AddEnemy"), args);

			AActor* AttackTargetActor = TargetEntity->Actor();
			OwnerComp.GetBlackboardComponent()->SetValueAsObject(FName("AttackTargetActor"), AttackTargetActor);
			OwnerComp.GetBlackboardComponent()->SetValueAsInt(FName("AttackEntityID"), TargetEntity->ID());
			FindTarget = true;
		}
	}
	else
	{
		//近战兵选择最近的敌人
		FVector EntityPos = entity->LocalPosition();
		float AttackRange = OwnerComp.GetBlackboardComponent()->GetValueAsFloat(FName("AttackRange"));
		if (AttackEntityID != 0)
		{
			GameObject* AttackEntity = static_cast<GameObject*>(UGolbalBPFunctionLibrary::FindEntity(AttackEntityID));
			if (AttackEntity != nullptr && !AttackEntity->IsState(ENTITY_STATE::EntityStateDead) && FVector::Dist2D(EntityPos, AttackEntity->LocalPosition()) <= AttackRange )
			{
				return;
			}
		}

		TArray<CS3Entity*> TempList = UGolbalBPFunctionLibrary::GetCS3EntitysInRange("", SearchRange, actor->GetActorLocation());
		//因为后面使用Pop取元素，这里按照由远到近进行排序
		TempList.Sort([&EntityPos](CS3Entity& EntityA, CS3Entity& EntityB)
			{
				return FVector::Dist2D(EntityPos, EntityA.LocalPosition()) > FVector::Dist2D(EntityPos, EntityB.LocalPosition());
			});
		//for (int i=0; i<TempList.Num()-1; i++)
		//{
		//	for (int j = i + 1; j <= TempList.Num() - 1; j++)
		//	{

		//		if (FVector::Dist2D(TempList[i]->LocalPosition(), entity->LocalPosition()) < FVector::Dist2D(TempList[j]->LocalPosition(), entity->LocalPosition()))
		//		{
		//			CS3Entity* tempPtr = TempList[j];
		//			TempList[j] = TempList[i];
		//			TempList[i] = tempPtr;
		//		}
		//	}
		//}

		while (TempList.Num())
		{
			GameObject* TargetEntity = static_cast<GameObject*>(TempList.Pop());
			UGameObjectInterface* TargetInterface = TargetEntity->Interface_Cache.GameObjectInterface;

			if (TargetEntity->IsState(ENTITY_STATE::EntityStateDead) || !enemyTypes.Contains(TargetInterface->getEntityFlag()))
			{
				continue;
			}
			if (TargetEntity->ID() == entity->ID())
			{
				continue;
			}
			int32 id = TargetEntity->ID();
			COMBAT_RELATION relation = entity->QueryRelation(TargetEntity);
			if (relation == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				KBEngine::FVariantArray args;
				args.Add(TargetEntity->ID());
				entity->CellCall(TEXT("CAI_AddEnemy"), args);

				AActor* AttackTargetActor = TargetEntity->Actor();
				OwnerComp.GetBlackboardComponent()->SetValueAsObject(FName("AttackTargetActor"), AttackTargetActor);
				OwnerComp.GetBlackboardComponent()->SetValueAsInt(FName("AttackEntityID"), TargetEntity->ID());
				FindTarget = true;
				break;
			}
		}
	}

	if (!FindTarget) {
		OwnerComp.GetBlackboardComponent()->ClearValue(FName("AttackTargetActor"));
		OwnerComp.GetBlackboardComponent()->SetValueAsObject(FName("AttackTargetActor"), nullptr);
		OwnerComp.GetBlackboardComponent()->SetValueAsInt(FName("AttackEntityID"), 0);
		actor->GetCharacterMovement()->bUseRVOAvoidance = false;
	}
	else
	{
		actor->GetCharacterMovement()->bUseRVOAvoidance = true;
	}
}
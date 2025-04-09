// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Ser_ChaseTarget.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDefault.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "CS3Base/CS3Entity.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Entity/Monster/CMonster.h"
#include "AIController.h"
#include "Actor/Monster/MonsterCharacter.h"


void UMAI_Ser_ChaseTarget::TickNode(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory, float DeltaSeconds)
{
	Super::TickNode(OwnerComp, NodeMemory, DeltaSeconds);
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	CMonster* entity = static_cast<CMonster*>(actor->GetSelfEntity());

	//取出现有的攻击对象ID
	int32 attackID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
	CS3Entity* attackEntity = static_cast<CS3Entity*>(UGolbalBPFunctionLibrary::FindEntity(attackID));
	if (attackEntity != nullptr && entity->QueryRelation(attackEntity) == COMBAT_RELATION::COMBAT_RELATION_ENEMY) //有效攻击对象
	{
		UCMonsterInterface* intf = Cast< UCMonsterInterface >( UGolbalBPFunctionLibrary::GetInterfaceByName( TEXT( "GameObjectInterface" ), entity->ID()) );
		intf->ChaseActor_Implementation(attackID);
	}
}
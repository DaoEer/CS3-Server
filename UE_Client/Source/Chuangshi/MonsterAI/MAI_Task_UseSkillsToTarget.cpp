// Fill out your copyright notice in the Description page of Project Settings.


#include "MAI_Task_UseSkillsToTarget.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "GameData/GameDefault.h"
#include "GameData/GameDeFine.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CS3Base/CS3Entity.h"
#include "Entity/Monster/CMonster.h"
#include "Util/CS3Debug.h"
#include "AIController.h"
#include "BehaviorTree/BehaviorTreeComponent.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "Actor/Monster/MonsterCharacter.h"


EBTNodeResult::Type UMAI_Task_UseSkillsToTarget::ExecuteTask(UBehaviorTreeComponent& OwnerComp, uint8* NodeMemory)
{
	AMonsterCharacter* actor = Cast<AMonsterCharacter>(OwnerComp.GetAIOwner()->GetPawn());
	if (!IsValid(actor))
	{
		return EBTNodeResult::Failed;
	}
	CMonster* entity = static_cast<CMonster*>(actor->GetSelfEntity());
	if (!entity)
	{
		return EBTNodeResult::Failed;
	}
	UCSkillInterface* skillIntf = Cast< UCSkillInterface >(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), entity->ID()));
	if (!IsValid(skillIntf) || skillIntf->isCastingSkill())
	{
		return EBTNodeResult::Failed;
	}

	//取出现有的攻击对象ID
	int32 attackID = OwnerComp.GetBlackboardComponent()->GetValueAsInt(FName("AttackEntityID"));
	if (attackID == 0)
	{
		return EBTNodeResult::Failed;
	}
	CS3Entity* attackEntity = static_cast<CS3Entity*>(UGolbalBPFunctionLibrary::FindEntity(attackID));
	if (attackEntity == nullptr)
	{
		return EBTNodeResult::Failed;
	}
	if ( entity->QueryRelation(attackEntity) != COMBAT_RELATION::COMBAT_RELATION_ENEMY) //有效攻击对象
	{
		return EBTNodeResult::Failed;
	}

	int32 SkillID = entity->GetGroupSkillID();
	skillIntf->useCSkillToEntity(SkillID, attackID);
	//skillIntf->useCSkillToEntity( 993001001, attackID);


	return EBTNodeResult::Succeeded;


}
#pragma once
#include"CMonsterGroup.h"
#include "KBEngine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/CMonsterInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "AIController.h"
#include "MonsterAI/MonsterAIController.h"
#include "BehaviorTree/BlackboardComponent.h"
#include "BehaviorTree/BehaviorTree.h"
#include "Entity/Monster/CMonster.h"



/*
* 文件名称：CMonsterGroup.h
* 功能说明：集群CMonster
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-15
*/

void CMonsterGroup::AddMember(FString ScriptID, int32 MemberID) {
	if (!GroupData.Contains(ScriptID))
	{
		GroupData.Add(ScriptID);
	}
	GroupData[ScriptID].AddUnique(MemberID);
	
}

void CMonsterGroup::RemoveMember(FString ScriptID, int32 MemberID) {

}

void CMonsterGroup::CmdFollow(int32 FollowID) {
	//初始化 行数 列数 当前行个数 每行最大个数
	char row=0, column=-1;
	char maxNum = 5;
	//每个兵之间的间隔 1.5米
	float distance = 200.f;
	//与目标的初始距离 3.0米
	float extension = 300.f;

	for (TMap<FString, TArray<int32>>::TConstIterator miter(GroupData); miter; ++miter)
	{
		for (TArray<int32>::TConstIterator aiter = miter.Value().CreateConstIterator(); aiter; ++aiter)
		{
			int32 _entityID = *aiter;
			KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(_entityID);
			if (entity)
			{
				
				CMonster* monster = static_cast<CMonster*>(entity);
				if (monster)
				{
					column++;
					if (column == maxNum) {
						row++;
						column = 0;
					}
					
					KBEngine::FVariantArray Args;
					float rowLen = row * distance;
					float columnLen = column * distance;
					Args.Add(FollowID);
					Args.Add(rowLen);
					Args.Add(columnLen);
					Args.Add(extension);

					monster->ReciveControlCMD(MONSTER_AI_COMMAND::FOLLOW, Args);

				}
			}
			
		}
	}
}

void CMonsterGroup::CmdAttack()
{
	for (TMap<FString, TArray<int32>>::TConstIterator miter(GroupData); miter; ++miter)
	{
		for (TArray<int32>::TConstIterator aiter = miter.Value().CreateConstIterator(); aiter; ++aiter)
		{
			int32 _entityID = *aiter;
			KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(_entityID);
			if (entity)
			{
				CMonster* monster = static_cast<CMonster*>(entity);
				if (monster)
				{
					AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(monster->Actor());
					if (IsValid(MonsterCharacter))
					{
						AMonsterAIController* AIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
						AIController->StopMovement();
						if (AIController->behaviorComponent)
						{
							UBlackboardComponent* BlackboardComp = AIController->behaviorComponent->GetBlackboardComponent();
							if (BlackboardComp)
							{
								BlackboardComp->SetValueAsInt(FName("AttackEntityID"), 0);
								monster->ReciveControlCMD(MONSTER_AI_COMMAND::ATTACK);
							}
						}
						
					}
					
				}
			}

		}
	}
}


void CMonsterGroup::CmdUseSkill()
{
	for (TMap<FString, TArray<int32>>::TConstIterator miter(GroupData); miter; ++miter) {
		for (TArray<int32>::TConstIterator aiter(miter.Value()); aiter; ++aiter) {
			int32 EntityID = *aiter;
			KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(EntityID);
			if (pEntity) {
				CMonster* pCMonster = static_cast<CMonster*>(pEntity);
				pCMonster ? pCMonster->ReciveControlCMD(MONSTER_AI_COMMAND::NONE) : NULL;
			}
		}
	}
	
}

void CMonsterGroup::CmdArrayRectangle(FVector CenterLocation, FRotator CenterRotation)
{
	////初始化 当前行数 当前列数 每行最大列数
	//char Row = 0, Column = -1, ColumnMax = 5;

	//for (TMap<FString, TArray<int32>>::TConstIterator IterMap(GroupData); IterMap; ++IterMap){
	//	for (TArray<int32>::TConstIterator IterArr = IterMap.Value().CreateConstIterator(); IterArr; ++IterArr){
	//		int32 EntityID = *IterArr;
	//		KBEngine::Entity* pEntity = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	//		if (pEntity){
	//			CMonster* pCMonster = static_cast<CMonster*>(pEntity);
	//			if (pCMonster){
	//				Column++;
	//				if (Column == ColumnMax){
	//					Row++;
	//					Column = 0;
	//				}

	//				KBEngine::FVariantArray Args;
	//				Args.Add(CenterLocation);
	//				Args.Add(CenterRotation);
	//				Args.Add(Row);
	//				Args.Add(Column);



	//				pCMonster->ReciveControlCMD(MONSTER_AI_COMMAND::ARRAY_RECT, Args);

	//			}
	//		}

	//	}
	//}
}


void CMonsterGroup::CmdArrayCircle() {

}



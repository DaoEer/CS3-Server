// Fill out your copyright notice in the Description page of Project Settings.


#include "CMonsterAIInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterAI/MonsterAIController.h"
#include "MonsterAI/MonsterAIEnum.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UCMonsterAIInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UCMonsterAIInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(cMonsterAIState, &UCMonsterAIInterface::Set_cMonsterAIState, uint8)
CS3_END_INTERFACE_PROPERTY_MAP()


void UCMonsterAIInterface::Set_cMonsterAIState(const uint8& newVal, const uint8& oldVal)
{
	if (GetEntity())
	{
		if (int32(GetEntity()->GetDefinedProperty(TEXT("controlEntityID"))) == UGolbalBPFunctionLibrary::GetPlayerID())
		{
			AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
			if (IsValid(MonsterCharacter))
			{
				AMonsterAIController* MonsterAIController = Cast<AMonsterAIController>(MonsterCharacter->GetController());
				if (IsValid(MonsterAIController))
				{
					uint8 AIState = uint8(GetEntity()->GetDefinedProperty(TEXT("cMonsterAIState")));
					MonsterAIController->blackboardComponent->SetValueAsEnum(FName("CurrAIState"), uint8(MONSTER_AI_STATE(AIState)));
				}
			}

		}
	}
}
// Fill out your copyright notice in the Description page of Project Settings.


#include "CMonsterCombatInterface.h"
#include "Actor/Monster/MonsterCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UCMonsterCombatInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UCMonsterCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &UCMonsterCombatInterface::Set_HP, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP_Max, &UCMonsterCombatInterface::Set_HP_Max, int32)
CS3_END_INTERFACE_PROPERTY_MAP()


void UCMonsterCombatInterface::Set_HP(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnHPChanged(HP, HP_Max);
		}

	}

}

void UCMonsterCombatInterface::Set_HP_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP_Max(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnHPChanged(HP, HP_Max);
		}

	}
}

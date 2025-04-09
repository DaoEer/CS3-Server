// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtShowTopCountDownInterface.h"
#include "Actor/Monster/MonsterCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtShowTopCountDownInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtShowTopCountDownInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtShowTopCountDownInterface::UMonsterExtShowTopCountDownInterface()
{
}

UMonsterExtShowTopCountDownInterface::~UMonsterExtShowTopCountDownInterface()
{

}

void UMonsterExtShowTopCountDownInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_ShowRemainLifeTime");
	Supper::InitBlueCB();
}

void UMonsterExtShowTopCountDownInterface::CLIENT_ShowRemainLifeTime_Implementation(const float & remainTime)
{
	if (IsValid(GetActor()))
	{
		AMonsterCharacter* MonsterActor = Cast<AMonsterCharacter>(GetActor());
		if (MonsterActor && this->GetEntity())
		{
			MonsterActor->ShowRemainLifeTime(remainTime);
		}
	}
}

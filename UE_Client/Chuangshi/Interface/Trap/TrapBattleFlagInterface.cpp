// Fill out your copyright notice in the Description page of Project Settings.


#include "TrapBattleFlagInterface.h"
#include "Actor/Trap/TrapCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTrapBattleFlagInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTrapBattleFlagInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTrapBattleFlagInterface::UTrapBattleFlagInterface()
{
}

UTrapBattleFlagInterface::~UTrapBattleFlagInterface()
{

}
void UTrapBattleFlagInterface::OnRep_occurProgress()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 occurProgress = GetEntity()->GetDefinedProperty(TEXT("occurProgress")).GetValue<int32>();
		int32 maxProgress = GetEntity()->GetDefinedProperty(TEXT("maxProgress")).GetValue<int32>();
		ATrapCharacter* trapActor = Cast<ATrapCharacter>(GetActor());
		if (trapActor)
		{
			trapActor->OnOccupyProgressChanged(occurProgress, maxProgress);
		}
	}
}

void UTrapBattleFlagInterface::OnRep_maxProgress()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 occurProgress = GetEntity()->GetDefinedProperty(TEXT("occurProgress")).GetValue<int32>();
		int32 maxProgress = GetEntity()->GetDefinedProperty(TEXT("maxProgress")).GetValue<int32>();
		ATrapCharacter* trapActor = Cast<ATrapCharacter>(GetActor());
		if (trapActor)
		{
			trapActor->OnOccupyProgressChanged(occurProgress, maxProgress);
		}
	}
}

void UTrapBattleFlagInterface::OnRep_barracksBelongType()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 barracksBelongType = GetEntity()->GetDefinedProperty(TEXT("barracksBelongType")).GetValue<int32>();
		ATrapCharacter* trapActor = Cast<ATrapCharacter>(GetActor());
		if (trapActor)
		{
			trapActor->OnOccupyBelongTypeChanged(barracksBelongType);
		}
	}
}


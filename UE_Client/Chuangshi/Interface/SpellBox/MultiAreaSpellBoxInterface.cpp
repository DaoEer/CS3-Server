// Fill out your copyright notice in the Description page of Project Settings.

#include "MultiAreaSpellBoxInterface.h"
#include "Actor/SpellBox/MultiAreaSpellBoxCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMultiAreaSpellBoxInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMultiAreaSpellBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UMultiAreaSpellBoxInterface::UMultiAreaSpellBoxInterface()
{
}

UMultiAreaSpellBoxInterface::~UMultiAreaSpellBoxInterface()
{
}

void UMultiAreaSpellBoxInterface::CLIENT_OnSwitchArea_Implementation(int32 areaIndex)
{
	if (IsValid(GetActor()))
	{
		AMultiAreaSpellBoxCharacter* MultiAreaSpellBoxCharacter = Cast<AMultiAreaSpellBoxCharacter>(GetActor());
		if (MultiAreaSpellBoxCharacter)
		{
			MultiAreaSpellBoxCharacter->OnSwitchArea(areaIndex);
		}
	}
}

void UMultiAreaSpellBoxInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnSwitchArea");
	Supper::InitBlueCB();
}

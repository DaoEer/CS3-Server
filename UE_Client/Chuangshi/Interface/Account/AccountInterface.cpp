// Fill out your copyright notice in the Description page of Project Settings.


#include "AccountInterface.h"
#include "JsonFieldData.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UAccountInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UAccountInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


UAccountInterface::UAccountInterface()
{
}

UAccountInterface::~UAccountInterface()
{
}

void UAccountInterface::OnRep_lastLogonDBID()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("--UAccountInterface::OnRep_lastLogonDBID no this Entity!%d"), EntityID);
		return;
	}
	uint64 newValue = GetEntity()->GetDefinedProperty(TEXT("lastLogonDBID")).GetValue<uint64>();
}


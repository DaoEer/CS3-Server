// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtDisposableInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtDisposableInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtDisposableInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtDisposableInterface::UMonsterExtDisposableInterface()
{
}

UMonsterExtDisposableInterface::~UMonsterExtDisposableInterface()
{

}

int32 UMonsterExtDisposableInterface::GetOwnerID()
{
	if (GetEntity() != nullptr)
	{
		return GetEntity()->GetDefinedProperty(TEXT("ownerID")).GetValue<int32>();
	}
	return 0;
}
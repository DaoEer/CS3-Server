// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtRHBInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtRHBInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtRHBInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtRHBInterface::UMonsterExtRHBInterface()
{
}
UMonsterExtRHBInterface::~UMonsterExtRHBInterface()
{
}
void UMonsterExtRHBInterface::startThorwtorch_Implementation(const FString& effectID, const int32& radius)
{
}

void UMonsterExtRHBInterface::InitBlueCB()
{
	ArrBlueFunc.Add("startThorwtorch");
	Supper::InitBlueCB();
}

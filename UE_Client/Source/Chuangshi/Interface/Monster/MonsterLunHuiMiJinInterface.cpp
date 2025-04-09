// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterLunHuiMiJinInterface.h"
#include "Actor/Monster/MonsterCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterLunHuiMiJinInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterLunHuiMiJinInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterLunHuiMiJinInterface::UMonsterLunHuiMiJinInterface()
{
}

UMonsterLunHuiMiJinInterface::~UMonsterLunHuiMiJinInterface()
{
}

void UMonsterLunHuiMiJinInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}
// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtCollisionCar.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtAttackCityLadderInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtCollisionCar, Supper)
DEF_INTERFACE(UMonsterExtAttackCityLadderInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtCollisionCar, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtCollisionCar, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtCollisionCar::MonsterExtCollisionCar()
{
}

MonsterExtCollisionCar::~MonsterExtCollisionCar()
{
}

UClass* MonsterExtCollisionCar::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtCollisionCar"));
}


CONTROL_COMPILE_OPTIMIZE_END

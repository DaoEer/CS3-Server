// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtAttackCityLadder.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtAttackCityLadderInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtAttackCityLadder, Supper)
DEF_INTERFACE(UMonsterExtAttackCityLadderInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtAttackCityLadder, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtAttackCityLadder, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtAttackCityLadder::MonsterExtAttackCityLadder()
{
}

MonsterExtAttackCityLadder::~MonsterExtAttackCityLadder()
{
}

UClass* MonsterExtAttackCityLadder::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtAttackCityLadder"));
}


CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtAerialLadder.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtAerialLadderInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtAerialLadder, Supper)
DEF_INTERFACE(UMonsterExtAerialLadderInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtAerialLadder, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtAerialLadder, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtAerialLadder::MonsterExtAerialLadder()
{
}

MonsterExtAerialLadder::~MonsterExtAerialLadder()
{
}

UClass* MonsterExtAerialLadder::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtAerialLadder"));
}


CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtBattery.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtBatteryInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtBattery, Supper)
DEF_INTERFACE( UMonsterExtBatteryInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtBattery, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtBattery, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtBattery::MonsterExtBattery()
{
}

MonsterExtBattery::~MonsterExtBattery()
{
}

UClass* MonsterExtBattery::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtBattery")); 
}


CONTROL_COMPILE_OPTIMIZE_END

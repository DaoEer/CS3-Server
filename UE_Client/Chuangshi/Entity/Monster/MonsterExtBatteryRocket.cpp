// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtBatteryRocket.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtBatteryInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtBatteryRocket, Supper)
DEF_INTERFACE( UMonsterExtBatteryInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtBatteryRocket, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtBatteryRocket, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtBatteryRocket::MonsterExtBatteryRocket()
{
}

MonsterExtBatteryRocket::~MonsterExtBatteryRocket()
{
}

UClass* MonsterExtBatteryRocket::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtBatteryRocket")); 
}


CONTROL_COMPILE_OPTIMIZE_END

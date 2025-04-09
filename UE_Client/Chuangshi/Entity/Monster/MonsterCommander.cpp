// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterCommander.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterCommander, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterCommander, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



UClass* MonsterCommander::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterCommander")); 
}


CONTROL_COMPILE_OPTIMIZE_END

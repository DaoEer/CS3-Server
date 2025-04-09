// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterSoldier.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterSoldier, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterSoldier, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



UClass* MonsterSoldier::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterSoldier")); 
}


CONTROL_COMPILE_OPTIMIZE_END

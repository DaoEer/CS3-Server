// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterJuMa.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterJuMa, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterJuMa, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterJuMa::MonsterJuMa()
{
}

MonsterJuMa::~MonsterJuMa()
{
}

UClass* MonsterJuMa::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterJuMa")); 
}


CONTROL_COMPILE_OPTIMIZE_END

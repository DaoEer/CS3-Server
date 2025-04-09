// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtCover.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtCover, Supper)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtCover, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtCover, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtCover::MonsterExtCover()
{
}

MonsterExtCover::~MonsterExtCover()
{
}

UClass* MonsterExtCover::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtCover"));
}


CONTROL_COMPILE_OPTIMIZE_END

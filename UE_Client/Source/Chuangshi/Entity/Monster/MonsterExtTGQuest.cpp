// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtTGQuest.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtTGQuest, Supper)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtTGQuest, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtTGQuest, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtTGQuest::MonsterExtTGQuest()
{
}

MonsterExtTGQuest::~MonsterExtTGQuest()
{
}

UClass* MonsterExtTGQuest::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Monster"));
}


CONTROL_COMPILE_OPTIMIZE_END

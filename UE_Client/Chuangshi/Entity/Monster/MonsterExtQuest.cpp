// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtQuest.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtQuest, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtQuest, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtQuest::MonsterExtQuest()
{
}

MonsterExtQuest::~MonsterExtQuest()
{
}

UClass* MonsterExtQuest::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtQuest")); 
}


CONTROL_COMPILE_OPTIMIZE_END

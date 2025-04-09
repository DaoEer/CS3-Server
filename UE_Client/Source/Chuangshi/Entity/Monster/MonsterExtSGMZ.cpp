// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtSGMZ.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtSGMZ, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtSGMZ, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtSGMZ::MonsterExtSGMZ()
{
}

MonsterExtSGMZ::~MonsterExtSGMZ()
{
}

UClass* MonsterExtSGMZ::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtSGMZ"));
}
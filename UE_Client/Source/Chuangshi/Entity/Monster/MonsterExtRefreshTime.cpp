// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtRefreshTime.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtRefreshTime, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtRefreshTime, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtRefreshTime::MonsterExtRefreshTime()
{
}

MonsterExtRefreshTime::~MonsterExtRefreshTime()
{
}

UClass* MonsterExtRefreshTime::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtRefreshTime"));
}
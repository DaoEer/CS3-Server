// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtClickAndModel.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtClickAndModel, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtClickAndModel, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtClickAndModel::MonsterExtClickAndModel()
{
}

MonsterExtClickAndModel::~MonsterExtClickAndModel()
{
}

UClass* MonsterExtClickAndModel::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtClickAndModel")); 
}
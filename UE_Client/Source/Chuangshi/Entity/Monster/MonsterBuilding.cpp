// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterBuilding.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterBuildingInterface.h"

DEF_INTERFACE_BEGIN(MonsterBuilding, Supper)
DEF_INTERFACE( UMonsterBuildingInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterBuilding, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterBuilding, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterBuilding::MonsterBuilding()
{
}

MonsterBuilding::~MonsterBuilding()
{
}

UClass* MonsterBuilding::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterBuilding")); 
}
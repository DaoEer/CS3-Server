// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtInteractive.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtInteractiveInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtInteractive, Supper)
DEF_INTERFACE( UMonsterExtInteractiveInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtInteractive, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtInteractive, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtInteractive::MonsterExtInteractive()
{
}

MonsterExtInteractive::~MonsterExtInteractive()
{
}

UClass* MonsterExtInteractive::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtInteractive"));
}
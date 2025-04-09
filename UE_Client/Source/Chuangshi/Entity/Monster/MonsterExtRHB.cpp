// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtRHB.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtRHBInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtRHB, Supper)
DEF_INTERFACE( UMonsterExtRHBInterface )
DEF_INTERFACE_END()
	
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtRHB, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtRHB, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtRHB::MonsterExtRHB()
{
}

MonsterExtRHB::~MonsterExtRHB()
{
}

UClass* MonsterExtRHB::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtRHB"));
}



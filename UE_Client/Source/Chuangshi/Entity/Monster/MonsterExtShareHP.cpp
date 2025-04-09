// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtShareHP.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtShareHPInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtShareHP, Supper)
DEF_INTERFACE( UMonsterExtShareHPInterface )
DEF_INTERFACE_END()
	
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtShareHP, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtShareHP, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtShareHP::MonsterExtShareHP()
{
}

MonsterExtShareHP::~MonsterExtShareHP()
{
}

UClass* MonsterExtShareHP::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtShareHP")); 
}
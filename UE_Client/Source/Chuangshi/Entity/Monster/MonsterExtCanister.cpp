// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtCanister.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtCanisterInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtCanister, Supper)
DEF_INTERFACE( UMonsterExtCanisterInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtCanister, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtCanister, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtCanister::MonsterExtCanister()
{
}

MonsterExtCanister::~MonsterExtCanister()
{
}

UClass* MonsterExtCanister::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtCanister"));
}


CONTROL_COMPILE_OPTIMIZE_END

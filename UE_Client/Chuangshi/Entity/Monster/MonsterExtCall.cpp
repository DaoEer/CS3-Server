// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtCall.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtCallInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtCall, Supper)
DEF_INTERFACE( UMonsterExtCallInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtCall, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtCall, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtCall::MonsterExtCall()
{
}

MonsterExtCall::~MonsterExtCall()
{
}

UClass* MonsterExtCall::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtCall")); 
}


CONTROL_COMPILE_OPTIMIZE_END

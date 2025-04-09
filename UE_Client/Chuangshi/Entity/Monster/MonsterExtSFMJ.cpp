// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtSFMJ.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtSFMJInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtSFMJ, Supper)
DEF_INTERFACE( UMonsterExtSFMJInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtSFMJ, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtSFMJ, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtSFMJ::MonsterExtSFMJ()
{
}

MonsterExtSFMJ::~MonsterExtSFMJ()
{
}

UClass* MonsterExtSFMJ::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtSFMJ"));
}
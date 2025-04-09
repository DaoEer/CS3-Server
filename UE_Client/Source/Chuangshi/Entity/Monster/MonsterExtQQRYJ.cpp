// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtQQRYJ.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtQQRYJInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtQQRYJ, Supper)
DEF_INTERFACE( UMonsterExtQQRYJInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtQQRYJ, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtQQRYJ, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtQQRYJ::MonsterExtQQRYJ()
{
}

MonsterExtQQRYJ::~MonsterExtQQRYJ()
{
}

UClass* MonsterExtQQRYJ::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtQQRYJ"));
}
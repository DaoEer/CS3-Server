// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterLunHuiMiJin.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterLunHuiMiJinInterface.h"

DEF_INTERFACE_BEGIN(MonsterLunHuiMiJin, Supper)
DEF_INTERFACE( UMonsterLunHuiMiJinInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterLunHuiMiJin, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterLunHuiMiJin, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterLunHuiMiJin::MonsterLunHuiMiJin()
{
}

MonsterLunHuiMiJin::~MonsterLunHuiMiJin()
{
}

UClass* MonsterLunHuiMiJin::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterLunHuiMiJin"));
}
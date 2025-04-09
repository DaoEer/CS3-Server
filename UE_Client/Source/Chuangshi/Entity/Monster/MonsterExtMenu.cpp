// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtMenu.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtMenu, Supper)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtMenu, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtMenu, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtMenu::MonsterExtMenu()
{
}

MonsterExtMenu::~MonsterExtMenu()
{
}

UClass* MonsterExtMenu::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtMenu")); 
}


CONTROL_COMPILE_OPTIMIZE_END

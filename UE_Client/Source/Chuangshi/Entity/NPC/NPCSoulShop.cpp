// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCSoulShop.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(NPCSoulShop, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCSoulShop, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCSoulShop::NPCSoulShop()
{
	_fActorName = FString("NPCSoulShop");
	//_fCompontentName = FName("UPlatformActorComponent");
}

NPCSoulShop::~NPCSoulShop()
{

}


UClass* NPCSoulShop::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}


CONTROL_COMPILE_OPTIMIZE_END

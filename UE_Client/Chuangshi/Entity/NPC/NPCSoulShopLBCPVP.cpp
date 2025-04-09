// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCSoulShopLBCPVP.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(NPCSoulShopLBCPVP, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCSoulShopLBCPVP, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCSoulShopLBCPVP::NPCSoulShopLBCPVP()
{
	_fActorName = FString("NPCSoulShopLBCPVP");
	//_fCompontentName = FName("UPlatformActorComponent");
}

NPCSoulShopLBCPVP::~NPCSoulShopLBCPVP()
{

}


UClass* NPCSoulShopLBCPVP::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}


CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.

#include "NPCExtMysteriousShop.h"
#include "Interface/NPC/NPCExtMysteriousShopInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(NPCExtMysteriousShop, Supper)
DEF_INTERFACE(UNPCExtMysteriousShopInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtMysteriousShop, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtMysteriousShop, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCExtMysteriousShop::NPCExtMysteriousShop()
{
	_fActorName = FString("NPCExtMysteriousShop");
	//_fCompontentName = FName("UPlatformActorComponent");
}

NPCExtMysteriousShop::~NPCExtMysteriousShop()
{

}


UClass* NPCExtMysteriousShop::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}


CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCNeuralShop.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(NPCNeuralShop, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCNeuralShop, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCNeuralShop::NPCNeuralShop()
{
	_fActorName = FString("NPCNeuralShop");
	//_fCompontentName = FName("UPlatformActorComponent");
}

NPCNeuralShop::~NPCNeuralShop()
{

}


UClass* NPCNeuralShop::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC")); 
}


CONTROL_COMPILE_OPTIMIZE_END

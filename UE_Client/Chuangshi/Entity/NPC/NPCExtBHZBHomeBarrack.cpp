// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCExtBHZBHomeBarrack.h"
#include "Util/GolbalBPFunctionLibrary.h"


DEF_INTERFACE_BEGIN(NPCExtBHZBHomeBarrack, Supper)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtBHZBHomeBarrack, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtBHZBHomeBarrack, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCExtBHZBHomeBarrack::NPCExtBHZBHomeBarrack()
{
	_fActorName = FString("NPCExtBHZBHomeBarrack");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = false;
}

NPCExtBHZBHomeBarrack::~NPCExtBHZBHomeBarrack()
{

}

UClass* NPCExtBHZBHomeBarrack::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPC"));
}

CONTROL_COMPILE_OPTIMIZE_END

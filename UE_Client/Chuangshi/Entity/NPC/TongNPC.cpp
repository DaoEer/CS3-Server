// Fill out your copyright notice in the Description page of Project Settings.


#include "TongNPC.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/TongNPCInterface.h"

DEF_INTERFACE_BEGIN(TongNPC, Supper)
DEF_INTERFACE(UTongNPCInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(TongNPC, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TongNPC, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


TongNPC::TongNPC()
{
	_fActorName = FString("TongNPC");
	//_fCompontentName = FName("UPlatformActorComponent");
}

TongNPC::~TongNPC()
{

}


UClass* TongNPC::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TongNPC")); 
}


CONTROL_COMPILE_OPTIMIZE_END

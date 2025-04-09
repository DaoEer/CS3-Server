// Fill out your copyright notice in the Description page of Project Settings.


#include "TeleportStone.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/TeleportStone/TeleportStoneInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(TeleportStone, Supper)
DEF_INTERFACE(UTeleportStoneInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(TeleportStone, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TeleportStone, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


TeleportStone::TeleportStone()
{
	_fActorName = FString("TeleportStone");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = true;
}

TeleportStone::~TeleportStone()
{

}


UClass* TeleportStone::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TeleportStone")); 
}

CONTROL_COMPILE_OPTIMIZE_END

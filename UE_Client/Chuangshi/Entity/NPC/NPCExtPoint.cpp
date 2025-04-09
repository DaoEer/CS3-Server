// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCExtPoint.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "../../Interface/NPC/NPCExtPointInterface.h"


DEF_INTERFACE_BEGIN(NPCExtPoint, Supper)
DEF_INTERFACE(UNPCExtPointInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtPoint, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtPoint, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCExtPoint::NPCExtPoint()
{
	_fActorName = FString("NPCExtPoint");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = false;
}

NPCExtPoint::~NPCExtPoint()
{

}

UClass* NPCExtPoint::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCExtPoint"));
}

CONTROL_COMPILE_OPTIMIZE_END

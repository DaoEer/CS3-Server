// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCTrainSoldierGround.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "../../Interface/NPC/NPCTrainSoldierGroundInterface.h"


DEF_INTERFACE_BEGIN(NPCTrainSoldierGround, Supper)
DEF_INTERFACE(UNPCTrainSoldierGroundInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCTrainSoldierGround, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCTrainSoldierGround, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCTrainSoldierGround::NPCTrainSoldierGround()
{
	_fActorName = FString("NPCTrainSoldierGround");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = false;
}

NPCTrainSoldierGround::~NPCTrainSoldierGround()
{

}

UClass* NPCTrainSoldierGround::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCTrainSoldierGround"));
}

CONTROL_COMPILE_OPTIMIZE_END

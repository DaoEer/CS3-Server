// Fill out your copyright notice in the Description page of Project Settings.


#include "NPCSeniorTrainSoldierGround.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "../../Interface/NPC/NPCTrainSoldierGroundInterface.h"


DEF_INTERFACE_BEGIN(NPCSeniorTrainSoldierGround, Supper)
DEF_INTERFACE(UNPCTrainSoldierGroundInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(NPCSeniorTrainSoldierGround, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCSeniorTrainSoldierGround, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


NPCSeniorTrainSoldierGround::NPCSeniorTrainSoldierGround()
{
	_fActorName = FString("NPCSeniorTrainSoldierGround");
	//_fCompontentName = FName("UNPCActorComponent");
	isOnGround_ = false;
}

NPCSeniorTrainSoldierGround::~NPCSeniorTrainSoldierGround()
{

}

UClass* NPCSeniorTrainSoldierGround::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCSeniorTrainSoldierGround"));
}

CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformShips.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformShipsInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformShips, Supper)
DEF_INTERFACE(UMovingPlatformShipsInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformShips, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformShips, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatformShips::MovingPlatformShips()
{
	_fActorName = FString("MovingPlatformShips");
	//_fCompontentName = FName("UPlatformActorComponent");
	isOnGround_ = false;
}

MovingPlatformShips::~MovingPlatformShips()
{

}


UClass* MovingPlatformShips::GetEntityModelClassAsset()
{

	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformShips"));
}


CONTROL_COMPILE_OPTIMIZE_END

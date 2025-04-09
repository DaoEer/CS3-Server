// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformShade.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformShadeInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformShade, Supper)
DEF_INTERFACE(UMovingPlatformShadeInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformShade, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformShade, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatformShade::MovingPlatformShade()
{
	_fActorName = FString("MovingPlatformShade");
	//_fCompontentName = FName("UPlatformActorComponent");
	isOnGround_ = false;
}

MovingPlatformShade::~MovingPlatformShade()
{

}


UClass* MovingPlatformShade::GetEntityModelClassAsset()
{

	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformShade")); 
}


CONTROL_COMPILE_OPTIMIZE_END

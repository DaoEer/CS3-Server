// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformRamp.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformRampInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformRamp, Supper)
DEF_INTERFACE(UMovingPlatformRampInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformRamp, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformRamp, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatformRamp::MovingPlatformRamp()
{
	_fActorName = FString("MovingPlatformRamp");
	//_fCompontentName = FName("UPlatformActorComponent");
	isOnGround_ = false;
}

MovingPlatformRamp::~MovingPlatformRamp()
{

}


UClass* MovingPlatformRamp::GetEntityModelClassAsset()
{

	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformRamp"));
}


CONTROL_COMPILE_OPTIMIZE_END

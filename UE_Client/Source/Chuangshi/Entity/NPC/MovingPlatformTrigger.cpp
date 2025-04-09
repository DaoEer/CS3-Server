// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatformTrigger.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformTriggerInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformTrigger, Supper)
DEF_INTERFACE(UMovingPlatformTriggerInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformTrigger, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformTrigger, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatformTrigger::MovingPlatformTrigger()
{
	_fActorName = FString("MovingPlatformTrigger");
	//_fCompontentName = FName("UPlatformActorComponent");
	isOnGround_ = false;
}

MovingPlatformTrigger::~MovingPlatformTrigger()
{

}


UClass* MovingPlatformTrigger::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformTrigger")); 
}


CONTROL_COMPILE_OPTIMIZE_END

// Fill out your copyright notice in the Description page of Project Settings.


#include "MovingPlatform.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatform, Supper)
DEF_INTERFACE(UMovingPlatformInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatform, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatform, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatform::MovingPlatform()
{
	_fActorName = FString("MovingPlatform");
	//_fCompontentName = FName("UPlatformActorComponent");
	isOnGround_ = false;
}

MovingPlatform::~MovingPlatform()
{

}


UClass* MovingPlatform::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatform")); 
}


CONTROL_COMPILE_OPTIMIZE_END

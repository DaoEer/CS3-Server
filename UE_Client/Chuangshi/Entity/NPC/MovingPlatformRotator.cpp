

#include "MovingPlatformRotator.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformRotatorInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformRotator, Supper)
DEF_INTERFACE(UMovingPlatformRotatorInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformRotator, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformRotator, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MovingPlatformRotator::MovingPlatformRotator()
{
	_fActorName = FString("MovingPlatformRotator");
	isOnGround_ = false;
}


MovingPlatformRotator::~MovingPlatformRotator()
{
}


UClass* MovingPlatformRotator::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformRotator"));
}

CONTROL_COMPILE_OPTIMIZE_END



#include "MovingPlatformLotus.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/NPC/MovingPlatformLotusInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformLotus, Supper)
DEF_INTERFACE(UMovingPlatformLotusInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformLotus, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformLotus, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MovingPlatformLotus::MovingPlatformLotus()
{
	_fActorName = FString("MovingPlatformLotus");
	isOnGround_ = false;
}


MovingPlatformLotus::~MovingPlatformLotus()
{
}


UClass* MovingPlatformLotus::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MovingPlatformLotus")); 
}

CONTROL_COMPILE_OPTIMIZE_END

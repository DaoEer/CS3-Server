
#include "PushTrap.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Trap/PushTrapInterface.h"

DEF_INTERFACE_BEGIN(PushTrap, Supper)
DEF_INTERFACE(UPushTrapInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(PushTrap, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(PushTrap, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

PushTrap::PushTrap()
{
	_fActorName = FString("PushTrap");
	//_fCompontentName = FName("UMoveTrapActorComponent");
}

PushTrap::~PushTrap()
{
}

UClass* PushTrap::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_PushTrap"));
}

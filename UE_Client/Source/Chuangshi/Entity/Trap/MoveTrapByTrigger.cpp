
#include "MoveTrapByTrigger.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Trap/MoveTrapByTriggerInterface.h"

DEF_INTERFACE_BEGIN(MoveTrapByTrigger, Supper)
DEF_INTERFACE(UMoveTrapByTriggerInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MoveTrapByTrigger, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MoveTrapByTrigger, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MoveTrapByTrigger::MoveTrapByTrigger()
{
	_fActorName = FString("MoveTrapByTrigger");
	//_fCompontentName = FName("UMoveTrapActorComponent");
}

MoveTrapByTrigger::~MoveTrapByTrigger()
{
}

UClass* MoveTrapByTrigger::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SKMesh_Trap")); 
}

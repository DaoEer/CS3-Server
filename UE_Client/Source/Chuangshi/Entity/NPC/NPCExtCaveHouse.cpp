#include "NPCExtCaveHouse.h"
#include "Interface/NPC/NPCExtCaveHouseInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(NPCExtCaveHouse, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(NPCExtCaveHouse, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(NPCExtCaveHouse, Supper)
DEF_INTERFACE(UNPCExtCaveHouseInterface)
DEF_INTERFACE_END()

NPCExtCaveHouse::NPCExtCaveHouse()
{
}

NPCExtCaveHouse::~NPCExtCaveHouse()
{
}

UClass* NPCExtCaveHouse::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_NPCExtCaveHouse"));
}

CONTROL_COMPILE_OPTIMIZE_END

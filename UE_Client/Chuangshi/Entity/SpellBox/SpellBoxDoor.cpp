
#include "SpellBoxDoor.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxDoor, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxDoor, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

SpellBoxDoor::SpellBoxDoor()
{
}

SpellBoxDoor::~SpellBoxDoor()
{
}

UClass* SpellBoxDoor::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxDoor"));
}
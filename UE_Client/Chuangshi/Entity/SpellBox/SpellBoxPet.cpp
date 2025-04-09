#include "SpellBoxPet.h"

#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxPet, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxPet, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



SpellBoxPet::SpellBoxPet()
{
}


SpellBoxPet::~SpellBoxPet()
{
}

UClass* SpellBoxPet::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxPet"));
}

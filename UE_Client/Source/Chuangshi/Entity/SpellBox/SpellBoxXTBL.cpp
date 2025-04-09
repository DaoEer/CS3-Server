#include "SpellBoxXTBL.h"

#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxXTBL, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxXTBL, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



SpellBoxXTBL::SpellBoxXTBL()
{
}


SpellBoxXTBL::~SpellBoxXTBL()
{
}

UClass* SpellBoxXTBL::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxXTBL"));
}

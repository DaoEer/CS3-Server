
#include "SpellBoxAdvanced.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/SpellBox/SpellBoxAdvancedInterface.h"

DEF_INTERFACE_BEGIN(SpellBoxAdvanced, Supper)
DEF_INTERFACE(USpellBoxAdvancedInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxAdvanced, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxAdvanced, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

SpellBoxAdvanced::SpellBoxAdvanced()
{
}

SpellBoxAdvanced::~SpellBoxAdvanced()
{
}

UClass* SpellBoxAdvanced::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxAdvanced"));
}
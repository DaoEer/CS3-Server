#include "SpellBoxLingTian.h"
#include "Interface/SpellBox/SpellBoxLingTianInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxLingTian, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxLingTian, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(SpellBoxLingTian, Supper)
DEF_INTERFACE(USpellBoxLingTianInterface)
DEF_INTERFACE_END()



SpellBoxLingTian::SpellBoxLingTian()
{
}


SpellBoxLingTian::~SpellBoxLingTian()
{
}

UClass* SpellBoxLingTian::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxLingTian"));
}

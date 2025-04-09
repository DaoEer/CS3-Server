#include "SpellBoxHasCreator.h"

#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxHasCreator, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxHasCreator, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



SpellBoxHasCreator::SpellBoxHasCreator()
{
}


SpellBoxHasCreator::~SpellBoxHasCreator()
{
}

UClass* SpellBoxHasCreator::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxHasCreator"));
}

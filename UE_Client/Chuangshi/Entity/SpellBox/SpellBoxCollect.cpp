#include "SpellBoxCollect.h"

#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(SpellBoxCollect, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(SpellBoxCollect, Supper)
KBE_END_ENTITY_PROPERTY_MAP()



SpellBoxCollect::SpellBoxCollect()
{
}


SpellBoxCollect::~SpellBoxCollect()
{
}

UClass* SpellBoxCollect::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_SpellBoxCollect"));
}


#include "MultiAreaSpellBox.h"
#include "Interface/SpellBox/MultiAreaSpellBoxInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MultiAreaSpellBox, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MultiAreaSpellBox, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(MultiAreaSpellBox, Supper)
DEF_INTERFACE(UMultiAreaSpellBoxInterface)
DEF_INTERFACE_END()

MultiAreaSpellBox::MultiAreaSpellBox()
{
}

MultiAreaSpellBox::~MultiAreaSpellBox()
{
}

UClass* MultiAreaSpellBox::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MultiAreaSpellBox"));
}

#include "TrapSymbolJade.h"
#include "../../Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(TrapSymbolJade, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TrapSymbolJade, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

TrapSymbolJade::TrapSymbolJade()
{
}

TrapSymbolJade::~TrapSymbolJade()
{
}
UClass* TrapSymbolJade::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TrapSymbolJade"));
}


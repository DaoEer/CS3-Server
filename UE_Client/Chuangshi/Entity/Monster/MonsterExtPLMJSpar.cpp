

#include "MonsterExtPLMJSpar.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtPLMJSpar, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtPLMJSpar, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtPLMJSpar::MonsterExtPLMJSpar()
{
}

MonsterExtPLMJSpar::~MonsterExtPLMJSpar()
{
}

UClass* MonsterExtPLMJSpar::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Monster"));
}



CONTROL_COMPILE_OPTIMIZE_END



#include "MonsterExtYXLMSoldier.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtYXLMSoldier, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtYXLMSoldier, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtYXLMSoldier::MonsterExtYXLMSoldier()
{
}

MonsterExtYXLMSoldier::~MonsterExtYXLMSoldier()
{
}

UClass* MonsterExtYXLMSoldier::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtYXLMSoldier"));
}



CONTROL_COMPILE_OPTIMIZE_END

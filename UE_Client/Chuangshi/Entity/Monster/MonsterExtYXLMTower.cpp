

#include "MonsterExtYXLMTower.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtYXLMTower, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtYXLMTower, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtYXLMTower::MonsterExtYXLMTower()
{
}

MonsterExtYXLMTower::~MonsterExtYXLMTower()
{
}

UClass* MonsterExtYXLMTower::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtYXLMTower")); 
}



CONTROL_COMPILE_OPTIMIZE_END

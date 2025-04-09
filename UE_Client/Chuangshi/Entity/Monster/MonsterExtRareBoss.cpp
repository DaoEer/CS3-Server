
#include "MonsterExtRareBoss.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtRareBoss, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtRareBoss, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtRareBoss::MonsterExtRareBoss()
{
}


MonsterExtRareBoss::~MonsterExtRareBoss()
{
}
UClass* MonsterExtRareBoss::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtRareBoss"));
}

CONTROL_COMPILE_OPTIMIZE_END

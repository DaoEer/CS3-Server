
#include "MonsterExtFirstTongStarcraftBoss.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtFirstTongStarcraftBoss, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtFirstTongStarcraftBoss, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtFirstTongStarcraftBoss::MonsterExtFirstTongStarcraftBoss()
{
}


MonsterExtFirstTongStarcraftBoss::~MonsterExtFirstTongStarcraftBoss()
{
}
UClass* MonsterExtFirstTongStarcraftBoss::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Monster"));
}

CONTROL_COMPILE_OPTIMIZE_END

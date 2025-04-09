
#include "MonsterExtImpact.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtImpactInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtImpact, Supper)
DEF_INTERFACE( UMonsterExtImpactInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtImpact, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtImpact, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtImpact::MonsterExtImpact()
{
}


MonsterExtImpact::~MonsterExtImpact()
{
}
UClass* MonsterExtImpact::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtImpact")); 
}

CONTROL_COMPILE_OPTIMIZE_END

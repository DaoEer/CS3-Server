

#include "MonsterExtChartlet.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtChartletInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtChartlet, Supper)
DEF_INTERFACE( UMonsterExtChartletInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtChartlet, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtChartlet, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtChartlet::MonsterExtChartlet()
{
}


MonsterExtChartlet::~MonsterExtChartlet()
{
}
UClass* MonsterExtChartlet::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtChartlet")); 
}
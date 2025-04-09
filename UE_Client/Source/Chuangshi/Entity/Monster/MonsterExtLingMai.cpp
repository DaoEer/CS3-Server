

#include "MonsterExtLingMai.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtLingMaiInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtLingMai, Supper)
DEF_INTERFACE(UMonsterExtLingMaiInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtLingMai, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtLingMai, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtLingMai::MonsterExtLingMai()
{
}


MonsterExtLingMai::~MonsterExtLingMai()
{
}
UClass* MonsterExtLingMai::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtLingMai"));
}
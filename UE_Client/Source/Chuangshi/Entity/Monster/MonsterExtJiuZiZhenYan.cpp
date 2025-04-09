

#include "MonsterExtJiuZiZhenYan.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtJiuZiZhenYanInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtJiuZiZhenYan, Supper)
DEF_INTERFACE( UMonsterExtJiuZiZhenYanInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJiuZiZhenYan, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJiuZiZhenYan, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJiuZiZhenYan::MonsterExtJiuZiZhenYan()
{
}


MonsterExtJiuZiZhenYan::~MonsterExtJiuZiZhenYan()
{
}
UClass* MonsterExtJiuZiZhenYan::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJiuZiZhenYan"));
}
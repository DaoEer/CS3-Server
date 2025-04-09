

#include "MonsterExtJZZYXY.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtJZZYXYInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtJZZYXY, Supper)
DEF_INTERFACE( UMonsterExtJZZYXYInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJZZYXY, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJZZYXY, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJZZYXY::MonsterExtJZZYXY()
{
}

MonsterExtJZZYXY::~MonsterExtJZZYXY()
{
}
UClass* MonsterExtJZZYXY::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJZZYXY"));
}
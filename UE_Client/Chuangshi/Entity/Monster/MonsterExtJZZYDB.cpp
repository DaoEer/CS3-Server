

#include "MonsterExtJZZYDB.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtJZZYDBInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtJZZYDB, Supper)
DEF_INTERFACE( UMonsterExtJZZYDBInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJZZYDB, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJZZYDB, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJZZYDB::MonsterExtJZZYDB()
{
}


MonsterExtJZZYDB::~MonsterExtJZZYDB()
{
}
UClass* MonsterExtJZZYDB::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJZZYDB"));
}
#include "MonsterExtArmorLock.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtArmorLockInterface.h"

DEF_INTERFACE_BEGIN(MonsterExtArmorLock, Supper)
DEF_INTERFACE( UMonsterExtArmorLockInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtArmorLock, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtArmorLock, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtArmorLock::MonsterExtArmorLock()
{
}


MonsterExtArmorLock::~MonsterExtArmorLock()
{
}

UClass* MonsterExtArmorLock::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtArmorLock"));
}

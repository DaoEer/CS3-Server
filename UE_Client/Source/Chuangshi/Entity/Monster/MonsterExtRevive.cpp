
#include "MonsterExtRevive.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

#include "Interface/Monster/MonsterExtReviveInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
DEF_INTERFACE_BEGIN(MonsterExtRevive, Supper)
DEF_INTERFACE( UMonsterExtReviveInterface )
DEF_INTERFACE_END()
	
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtRevive, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtRevive, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MonsterExtRevive::MonsterExtRevive()
{
}


MonsterExtRevive::~MonsterExtRevive()
{
}
UClass* MonsterExtRevive::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtRevive")); 
}

CONTROL_COMPILE_OPTIMIZE_END

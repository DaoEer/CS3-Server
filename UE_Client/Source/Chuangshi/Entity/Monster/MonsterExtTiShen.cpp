

#include "MonsterExtTiShen.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtTiShenInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
	
DEF_INTERFACE_BEGIN(MonsterExtTiShen, Supper)
DEF_INTERFACE( UMonsterExtTiShenInterface )
DEF_INTERFACE_END()
		
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtTiShen, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtTiShen, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtTiShen::MonsterExtTiShen()
{
}

MonsterExtTiShen::~MonsterExtTiShen()
{
}

UClass* MonsterExtTiShen::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtTiShen")); 
}



CONTROL_COMPILE_OPTIMIZE_END

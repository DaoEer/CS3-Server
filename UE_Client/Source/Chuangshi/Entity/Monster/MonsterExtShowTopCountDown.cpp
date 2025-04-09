

#include "MonsterExtShowTopCountDown.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtShowTopCountDownInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
	
DEF_INTERFACE_BEGIN(MonsterExtShowTopCountDown, Supper)
DEF_INTERFACE( UMonsterExtShowTopCountDownInterface )
DEF_INTERFACE_END()
	
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtShowTopCountDown, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtShowTopCountDown, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtShowTopCountDown::MonsterExtShowTopCountDown()
{
}

MonsterExtShowTopCountDown::~MonsterExtShowTopCountDown()
{
}

UClass* MonsterExtShowTopCountDown::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtShowTopCountDown"));
}



CONTROL_COMPILE_OPTIMIZE_END

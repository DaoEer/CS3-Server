

#include "MonsterExtMachine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtMachineInterface.h"
	
CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MonsterExtMachine, Supper)
DEF_INTERFACE( UMonsterExtMachineInterface )
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtMachine, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtMachine, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtMachine::MonsterExtMachine()
{
}

MonsterExtMachine::~MonsterExtMachine()
{
}

UClass* MonsterExtMachine::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtMachine")); 
}



CONTROL_COMPILE_OPTIMIZE_END

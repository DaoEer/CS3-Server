
#include "MonsterExtClickAndInteractive.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/InterfaceDef.h"
#include "Util/CS3Debug.h"
#include "Interface/Monster/MonsterExtClickAndInteractiveInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtClickAndInteractive, Supper)
KBE_END_ENTITY_METHOD_MAP()

DEF_INTERFACE_BEGIN(MonsterExtClickAndInteractive, Supper)
DEF_INTERFACE(UMonsterExtClickAndInteractiveInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtClickAndInteractive, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtClickAndInteractive::MonsterExtClickAndInteractive()
{

}

MonsterExtClickAndInteractive::~MonsterExtClickAndInteractive()
{

}

UClass* MonsterExtClickAndInteractive::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtClickAndInteractive"));
}
CONTROL_COMPILE_OPTIMIZE_END
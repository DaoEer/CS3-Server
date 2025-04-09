#include "MonsterExtFireCow.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtFireCowInterface.h"

CONTROL_COMPILE_OPTIMIZE_START
DEF_INTERFACE_BEGIN(MonsterExtFireCow, Supper)
DEF_INTERFACE(UMonsterExtFireCowInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtFireCow, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtFireCow, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtFireCow::MonsterExtFireCow()
{

}

MonsterExtFireCow::~MonsterExtFireCow()
{

}

UClass* MonsterExtFireCow::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtFireCow"));
}

CONTROL_COMPILE_OPTIMIZE_END
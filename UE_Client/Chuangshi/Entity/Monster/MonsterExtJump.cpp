#include "MonsterExtJump.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJump, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJump, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJump::MonsterExtJump()
{
}


MonsterExtJump::~MonsterExtJump()
{
}

UClass* MonsterExtJump::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJump"));
}

CONTROL_COMPILE_OPTIMIZE_END

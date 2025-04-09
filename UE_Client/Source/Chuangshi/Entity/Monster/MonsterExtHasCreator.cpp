#include "MonsterExtHasCreator.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtHasCreator, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtHasCreator, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtHasCreator::MonsterExtHasCreator()
{
}


MonsterExtHasCreator::~MonsterExtHasCreator()
{
}

UClass* MonsterExtHasCreator::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtHasCreator"));
}


CONTROL_COMPILE_OPTIMIZE_END



#include "MonsterClientBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterClientBase, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterClientBase, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterClientBase::MonsterClientBase()
{
}

MonsterClientBase::~MonsterClientBase()
{
}

UClass* MonsterClientBase::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterClientBase"));
}



CONTROL_COMPILE_OPTIMIZE_END

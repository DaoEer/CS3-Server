

#include "MonsterExtSYJZ.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtSYJZ, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtSYJZ, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtSYJZ::MonsterExtSYJZ()
{
}

MonsterExtSYJZ::~MonsterExtSYJZ()
{
}

UClass* MonsterExtSYJZ::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtSYJZ")); 
}



CONTROL_COMPILE_OPTIMIZE_END

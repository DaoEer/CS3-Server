

#include "MonsterExtChase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtChase, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtChase, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtChase::MonsterExtChase()
{
}

MonsterExtChase::~MonsterExtChase()
{
}

UClass* MonsterExtChase::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtChase")); 
}



CONTROL_COMPILE_OPTIMIZE_END

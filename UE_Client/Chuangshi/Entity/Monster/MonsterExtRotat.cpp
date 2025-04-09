

#include "MonsterExtRotat.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtRotat, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtRotat, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtRotat::MonsterExtRotat()
{
}

MonsterExtRotat::~MonsterExtRotat()
{
}

UClass* MonsterExtRotat::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtRotat")); 
}



CONTROL_COMPILE_OPTIMIZE_END

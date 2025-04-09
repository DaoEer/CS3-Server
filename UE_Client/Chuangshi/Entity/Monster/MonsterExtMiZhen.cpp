

#include "MonsterExtMiZhen.h"
#include "Util/GolbalBPFunctionLibrary.h"


KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtMiZhen, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtMiZhen, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtMiZhen::MonsterExtMiZhen()
{
}


MonsterExtMiZhen::~MonsterExtMiZhen()
{
}

UClass* MonsterExtMiZhen::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtMiZhen"));
}

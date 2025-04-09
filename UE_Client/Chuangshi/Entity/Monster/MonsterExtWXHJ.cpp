

#include "MonsterExtWXHJ.h"
#include "Util/GolbalBPFunctionLibrary.h"


KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtWXHJ, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtWXHJ, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtWXHJ::MonsterExtWXHJ()
{
}


MonsterExtWXHJ::~MonsterExtWXHJ()
{
}

UClass* MonsterExtWXHJ::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtWXHJ"));
}

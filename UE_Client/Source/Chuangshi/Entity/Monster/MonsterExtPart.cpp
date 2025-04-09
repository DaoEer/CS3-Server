#include "MonsterExtPart.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtPart, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtPart, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtPart::MonsterExtPart()
{
}


MonsterExtPart::~MonsterExtPart()
{
}

UClass* MonsterExtPart::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtPart"));
}
#include "MonsterExtMain.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtMain, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtMain, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtMain::MonsterExtMain()
{
}


MonsterExtMain::~MonsterExtMain()
{
}

UClass* MonsterExtMain::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtMain"));
}
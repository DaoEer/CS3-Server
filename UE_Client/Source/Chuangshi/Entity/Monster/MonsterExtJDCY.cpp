#include "MonsterExtJDCY.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJDCY, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJDCY, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJDCY::MonsterExtJDCY()
{

}

MonsterExtJDCY::~MonsterExtJDCY()
{

}

UClass* MonsterExtJDCY::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJDCY"));
}

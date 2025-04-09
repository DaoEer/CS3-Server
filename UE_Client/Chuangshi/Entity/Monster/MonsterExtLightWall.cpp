

#include "MonsterExtLightWall.h"
#include "Util/GolbalBPFunctionLibrary.h"


KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtLightWall, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtLightWall, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtLightWall::MonsterExtLightWall()
{
}


MonsterExtLightWall::~MonsterExtLightWall()
{
}

UClass* MonsterExtLightWall::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtLightWall"));
}

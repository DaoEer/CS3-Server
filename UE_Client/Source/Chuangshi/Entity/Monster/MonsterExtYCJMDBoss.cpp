

#include "MonsterExtYCJMDBoss.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtYCJMDBoss, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtYCJMDBoss, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtYCJMDBoss::MonsterExtYCJMDBoss()
{
}

MonsterExtYCJMDBoss::~MonsterExtYCJMDBoss()
{
}

UClass* MonsterExtYCJMDBoss::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtYCJMDBoss"));
}



CONTROL_COMPILE_OPTIMIZE_END

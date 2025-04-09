

#include "MonsterExtJingShiDongKu.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtJingShiDongKu, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtJingShiDongKu, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtJingShiDongKu::MonsterExtJingShiDongKu()
{
}

MonsterExtJingShiDongKu::~MonsterExtJingShiDongKu()
{
}

UClass* MonsterExtJingShiDongKu::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtJingShiDongKu"));
}



CONTROL_COMPILE_OPTIMIZE_END

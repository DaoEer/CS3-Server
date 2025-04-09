

#include "MonsterExtXuanTianBaoLu.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtXuanTianBaoLu, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtXuanTianBaoLu, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtXuanTianBaoLu::MonsterExtXuanTianBaoLu()
{
}

MonsterExtXuanTianBaoLu::~MonsterExtXuanTianBaoLu()
{
}

UClass* MonsterExtXuanTianBaoLu::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtXuanTianBaoLu"));
}



CONTROL_COMPILE_OPTIMIZE_END

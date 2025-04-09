

#include "MonsterExtFenHuoJinNiu.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtFenHuoJinNiu, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtFenHuoJinNiu, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtFenHuoJinNiu::MonsterExtFenHuoJinNiu()
{
}

MonsterExtFenHuoJinNiu::~MonsterExtFenHuoJinNiu()
{
}

UClass* MonsterExtFenHuoJinNiu::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtFenHuoJinNiu"));
}



CONTROL_COMPILE_OPTIMIZE_END

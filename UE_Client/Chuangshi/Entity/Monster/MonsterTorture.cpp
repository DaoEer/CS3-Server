

#include "MonsterTorture.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterTorture, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterTorture, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterTorture::MonsterTorture()
{
}

MonsterTorture::~MonsterTorture()
{
}

UClass* MonsterTorture::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterTorture")); 
}



CONTROL_COMPILE_OPTIMIZE_END

#include "MonsterExtCircleEffect.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtCircleEffect, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtCircleEffect, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtCircleEffect::MonsterExtCircleEffect()
{

}

MonsterExtCircleEffect::~MonsterExtCircleEffect()
{

}

UClass* MonsterExtCircleEffect::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtCircleEffect"));
}

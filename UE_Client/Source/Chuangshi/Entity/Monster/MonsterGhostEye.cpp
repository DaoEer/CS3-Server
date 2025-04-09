#include "MonsterGhostEye.h"
#include "Util/GolbalBPFunctionLibrary.h"

KBE_BEGIN_ENTITY_METHOD_MAP(MonsterGhostEye, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterGhostEye, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterGhostEye::MonsterGhostEye()
{

}

MonsterGhostEye::~MonsterGhostEye()
{

}

UClass* MonsterGhostEye::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("MonsterGhostEyeCharacter"));
}

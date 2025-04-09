

#include "MonsterExtXKTB.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtXKTBInterface.h"


KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtXKTB, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtXKTB, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(MonsterExtXKTB, Supper )
DEF_INTERFACE( UMonsterExtXKTBInterface)
DEF_INTERFACE_END()

MonsterExtXKTB::MonsterExtXKTB()
{
}


MonsterExtXKTB::~MonsterExtXKTB()
{
}

UClass* MonsterExtXKTB::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtXKTB"));
}

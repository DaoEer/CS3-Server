

#include "MonsterExtFenShen.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtFenShenInterface.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
	
DEF_INTERFACE_BEGIN(MonsterExtFenShen, Supper)
DEF_INTERFACE(UMonsterExtFenShenInterface)
DEF_INTERFACE_END()
		
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtFenShen, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtFenShen, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtFenShen::MonsterExtFenShen()
{
}

MonsterExtFenShen::~MonsterExtFenShen()
{
}

UClass* MonsterExtFenShen::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtFenShen")); 
}



CONTROL_COMPILE_OPTIMIZE_END

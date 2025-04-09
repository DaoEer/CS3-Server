

#include "MonsterExtDisposable.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Monster/MonsterExtDisposableInterface.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START
	
DEF_INTERFACE_BEGIN(MonsterExtDisposable, Supper)
DEF_INTERFACE(UMonsterExtDisposableInterface)
DEF_INTERFACE_END()
		
KBE_BEGIN_ENTITY_METHOD_MAP(MonsterExtDisposable, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MonsterExtDisposable, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

MonsterExtDisposable::MonsterExtDisposable()
{
}

MonsterExtDisposable::~MonsterExtDisposable()
{
}

UClass* MonsterExtDisposable::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_MonsterExtDisposable")); 
}



CONTROL_COMPILE_OPTIMIZE_END

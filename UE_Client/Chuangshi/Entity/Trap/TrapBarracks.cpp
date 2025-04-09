
#include "TrapBarracks.h"
#include "../../Util/GolbalBPFunctionLibrary.h"
#include "Interface/Trap/TrapBarracksInterface.h"


DEF_INTERFACE_BEGIN(TrapBarracks, Supper)
DEF_INTERFACE(UTrapBarracksInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(TrapBarracks, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(TrapBarracks, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

TrapBarracks::TrapBarracks()
{
}

TrapBarracks::~TrapBarracks()
{
}

UClass* TrapBarracks::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TrapBarracks"));
}


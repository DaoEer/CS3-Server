
#include "Trap.h"
#include "Interface/GameObjectInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Trap/TrapInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/StateInterface.h"


DEF_INTERFACE_BEGIN(Trap, Supper)
DEF_INTERFACE(UTrapInterface)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE(UStateInterface)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(Trap, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Trap, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

Trap::Trap()
{
	_fActorName = FString("Trap");
	//_fCompontentName = FName( "UTrapActorComponent" );
}

Trap::~Trap()
{
}


UClass* Trap::GetEntityModelClassAsset()
{
	UGameObjectInterface * Interface = Interface_Cache.GameObjectInterface;
	if (IsValid(Interface) && (Interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_CLIENT_TRIGGER_TRAP) || Interface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MOVE_TRAP)))
	{
		return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_ClientTrap")); 
	}
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Trap")); 
}

bool Trap::IsState(ENTITY_STATE EntityState)
{
	int32 State = GetDefinedProperty(TEXT("state")).GetValue<int32>();
	return State == int32(EntityState);
}



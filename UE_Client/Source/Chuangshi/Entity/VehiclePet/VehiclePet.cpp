
#include "VehiclePet.h"
#include "Actor/ServerCharacter.h"
#include "Interface/VehiclePet/VehiclePetInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CharacterRideManager.h"
#include "Util/CS3Debug.h"
#include "Interface/VehiclePet/VehiclePetInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/VehiclePet/PetStateInterface.h"
#include "Interface/VehiclePet/VehiclePetCombatInterface.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(VehiclePet, Supper)
DEF_INTERFACE(UVehiclePetInterface)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE(UPetStateInterface)
DEF_INTERFACE(UVehiclePetCombatInterface)
DEF_INTERFACE_END()


KBE_BEGIN_ENTITY_METHOD_MAP(VehiclePet, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(VehiclePet, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

VehiclePet::VehiclePet()
{
	_fActorName = FString("VehiclePet");
	//_fCompontentName = FName("UVehiclePetActorComponent");
}

VehiclePet::~VehiclePet()
{
}


void VehiclePet::DoCreateCharacter()
{
	Supper::DoCreateCharacter();

	FString scriptID = UGolbalBPFunctionLibrary::GetEntityPropertyValue(ID(), "scriptID");
	UUECS3GameInstance::Instance->CharacterRideManager->LoadRideAsset(scriptID);
}

UClass* VehiclePet::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_VehiclePet")); 
}

bool VehiclePet::IsState(ENTITY_STATE EntityState)
{
	int32 State = GetDefinedProperty(TEXT("state")).GetValue<int32>();
	return State == int32(EntityState);
}

CONTROL_COMPILE_OPTIMIZE_END

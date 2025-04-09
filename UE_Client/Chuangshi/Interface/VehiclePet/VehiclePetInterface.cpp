// Fill out your copyright notice in the Description page of Project Settings.


#include "VehiclePetInterface.h"
#include "Actor/ServerCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Interface/Role/RolePetInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UVehiclePetInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UVehiclePetInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UVehiclePetInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
	int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("baseOwnerID"));
	URolePetInterface* rolepetInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), ownerID));
	if (rolepetInterface)
	{
		rolepetInterface->OnSetOwnerPetID(0);
	}
}



void UVehiclePetInterface::OnRep_modelNumber()
{
	Supper::OnRep_modelNumber();
}

void UVehiclePetInterface::OnRep_modelScale()
{
	Supper::OnRep_modelScale();
}

void UVehiclePetInterface::OnRep_baseOwnerID()
{
	int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("baseOwnerID"));
	URolePetInterface* rolepetInterface = Cast<URolePetInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePetInterface"), ownerID));
	if (rolepetInterface)
	{
		rolepetInterface->OnSetOwnerPetID(EntityID);
	}
}

void UVehiclePetInterface::RPC_onSetPetControlledBy()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UVehiclePetInterface::RPC_onSetPetControlledBy : !GetEntity()"));
		return;
	}
	KBEngine::FVariantArray args;
	GetEntity()->CellCall(TEXT("onSetPetControlledBy"), args);
}
// Fill out your copyright notice in the Description page of Project Settings.


#include "VehiclePetCombatInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UVehiclePetCombatInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UVehiclePetCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &UVehiclePetCombatInterface::Set_HP, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP_Max, &UVehiclePetCombatInterface::Set_HP_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(camp, &UVehiclePetCombatInterface::Set_camp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue, &UVehiclePetCombatInterface::Set_gangQiValue, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue_Max, &UVehiclePetCombatInterface::Set_gangQiValue_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiState, &UVehiclePetCombatInterface::Set_gangQiState, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(tempCamp, &UVehiclePetCombatInterface::Set_tempCamp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQi_qiJieProgress, &UVehiclePetCombatInterface::Set_gangQi_qiJieProgress, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(title, &UVehiclePetCombatInterface::Set_title, FString)
CS3_END_INTERFACE_PROPERTY_MAP()


void UVehiclePetCombatInterface::Set_HP(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_HP_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP_Max(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_camp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_camp(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_gangQiValue(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue_Max(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_gangQiState(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiState(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_tempCamp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_tempCamp(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQi_qiJieProgress(newVal, oldVal);
}

void UVehiclePetCombatInterface::Set_title(const FString& newVal, const FString& oldVal)
{
	titleStr = newVal;
}
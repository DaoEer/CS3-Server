// Fill out your copyright notice in the Description page of Project Settings.
#include "StallState.h"

#include "Interface/Role/RoleStallInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"


void UStallState::Enter()
{
	if (CurrentEntity != nullptr)
	{
		URoleStallInterface* role = Cast<URoleStallInterface>(
			UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface"), CurrentEntity->ID()));
		if (role)
		{
			role->OnEnterStall();
		}
	}
}

void UStallState::Execute()
{

}

void UStallState::Exit()
{
	if (CurrentEntity != nullptr)
	{
		URoleStallInterface* role = Cast<URoleStallInterface>(
			UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleStallInterface"), CurrentEntity->ID()));
		if (role)
		{
			role->OnLevelStall();
		}
	}
}


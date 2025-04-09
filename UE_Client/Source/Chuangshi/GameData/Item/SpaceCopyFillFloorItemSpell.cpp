// Fill out your copyright notice in the Description page of Project Settings.

#include "SpaceCopyFillFloorItemSpell.h"
#include "../../Util/GolbalBPFunctionLibrary.h"
#include "../../Actor/Player/PlayerCharacter.h"
#include "../../Interface/Role/RoleSpaceContentInterface.h"

void USpaceCopyFillFloorItemSpell::SetUseItemToPositionBeforeNotifyServer()
{
	URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (interface)
	{
		interface->StartCheckFillFloor();
	}
}

void USpaceCopyFillFloorItemSpell::CancelUseItemToPositionBeforeNotifyServer()
{
	URoleSpaceContentInterface* interface = Cast<URoleSpaceContentInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceContentInterface")));
	if (interface)
	{
		interface->StopCheckFillFloor();
	}
}


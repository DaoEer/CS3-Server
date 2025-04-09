// Fill out your copyright notice in the Description page of Project Settings.


#include "ProtectedArea.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"


UProtectedArea::UProtectedArea()
{
}

UProtectedArea::~UProtectedArea()
{
}

void UProtectedArea::InitDatas(FAREA_DATA* AreaRow)
{
	UBaseArea::InitDatas(AreaRow);
	DeathHeight = AreaRow->DeathHeight;
	ReviveSpace = AreaRow->ReviveSpace;
	RevivePosition = AreaRow->RevivePosition;
	ReviveDirection = AreaRow->ReviveDirection;
}

bool UProtectedArea::IsPlayerUnder()
{
	if (FMath::IsNearlyZero(DeathHeight)) return false;//Î´ÅäÖÃËÀÍöÉî¶È
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())) return false;
	if (!IsPlayerIn()) return false;
	FVector PlayerPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	return PlayerPos.Z <= DeathHeight;
}

void UProtectedArea::Triger()
{
	int32 EntityID = UGolbalBPFunctionLibrary::GetPlayerID();
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		if (ReviveSpace.IsEmpty())
		{
			URoleSpaceInterface * RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityID));
			if (RoleSpaceInterface)
			{
				RoleSpaceInterface->RPC_requestGotoDynamicRevivePos();
			}
			//FVariantArray arg;
			//ent->CellCall(TEXT("requestGotoDynamicRevivePos"), arg);
		}
		else
		{
			URoleSpaceInterface * RoleSpaceInterface = Cast<URoleSpaceInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleSpaceInterface"), EntityID));
			if (RoleSpaceInterface)
			{
				RoleSpaceInterface->RPC_RequestGoToSpace(ReviveSpace, RevivePosition, ReviveDirection.Vector());
			}
			//TArray<FVariant> arg;
			//arg.Add(ReviveSpace);
			//arg.Add(RevivePosition);
			//arg.Add(ReviveDirection.Vector());
			//ent->CellCall(TEXT("requestGoToSpace"), arg);
		}
	}
}


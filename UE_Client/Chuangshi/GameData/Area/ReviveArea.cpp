// Fill out your copyright notice in the Description page of Project Settings.


#include "ReviveArea.h"
#include "Util/GolbalBPFunctionLibrary.h"

UReviveArea::UReviveArea()
{
}

UReviveArea::~UReviveArea()
{
}

void UReviveArea::InitDatas(FAREA_DATA* AreaRow)
{
	UBaseArea::InitDatas(AreaRow);
	DeathHeight = AreaRow->DeathHeight;
	ReviveSpace = AreaRow->ReviveSpace;
	RevivePosition = AreaRow->RevivePosition;
	ReviveDirection = AreaRow->ReviveDirection;
}

bool UReviveArea::IsPlayerUnder()
{
	if (FMath::IsNearlyZero(DeathHeight)) return false;//Î´ÅäÖÃËÀÍöÉî¶È
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())) return false;
	if (!IsPlayerIn()) return false;
	
	FVector PlayerPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	return PlayerPos.Z <= DeathHeight;
}

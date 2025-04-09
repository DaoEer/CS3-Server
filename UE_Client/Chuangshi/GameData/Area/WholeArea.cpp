// Fill out your copyright notice in the Description page of Project Settings.


#include "WholeArea.h"
#include "Util/GolbalBPFunctionLibrary.h"


UWholeArea::UWholeArea()
{
}

UWholeArea::~UWholeArea()
{
}

void UWholeArea::InitDatas(FAREA_DATA* AreaRow)
{
	UBaseArea::InitDatas(AreaRow);
	DeathHeight = AreaRow->DeathHeight;
	FlyHeight = AreaRow->FlyHeight;
}

bool UWholeArea::IsPointIn(FVector& Position)
{
	return true;
}

bool UWholeArea::IsPlayerUnder()
{
	if (!IsPlayerIn()) return false;
	if (FMath::IsNearlyZero(DeathHeight)) return false;//未配置死亡深度
	AActor* Player = Cast<AActor>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) return false;
	FVector PlayerPos = Player->GetActorLocation();
	return PlayerPos.Z <= DeathHeight;
}

bool UWholeArea::IsPlayerFlyCeiling()
{
	if (!IsPlayerIn()) return false;
	if (FMath::IsNearlyZero(FlyHeight)) return false;//未配置飞行深度
	AActor* Player = Cast<AActor>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player)) return false;
	FVector PlayerPos = Player->GetActorLocation();
	return FlyHeight <= PlayerPos.Z;
}

void UWholeArea::OnEnter(const FString SpaceScriptID)
{
}

// Fill out your copyright notice in the Description page of Project Settings.


#include "PlaneArea.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/CS3Debug.h"


UPlaneArea::UPlaneArea()
{
}

UPlaneArea::~UPlaneArea()
{
}

void UPlaneArea::InitDatas(FAREA_DATA* AreaRow)
{
	UBaseArea::InitDatas(AreaRow);
	VectPoly = AreaRow->Polygon;
	DeathHeight = AreaRow->DeathHeight;
	FlyHeight = AreaRow->FlyHeight;
}

void UPlaneArea::trriger(const FString SpaceScriptID)
{
	if (IsLock())return;
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(PlayerActor))
	{
		IsLock(true);
		Cast<APlayerCharacter>(PlayerActor)->OnTriggerPlane(SpaceScriptID);
	}
}

void UPlaneArea::OnEnter(const FString SpaceScriptID)
{
	IsLock(false);
	//UGolbalBPFunctionLibrary::StatusMessage(105, AreaName); //聊天框提示
}

bool UPlaneArea::IsPlayerCloseTo(float Distance)
{
	if (!IsPlayerIn()) return false;
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())) return false;
	FVector PlayerPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	return PolyPtr.Get()->IsCloseTo(PlayerPos, Distance);
}

bool UPlaneArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlaneArea::IsPlayerIn : PlayerActor!"));
		return false;
	}

	//获取当前Level
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (!level.Equals(MapScriptID))return false;

	FVector PlayerPosition = PlayerActor->GetActorLocation();
	return IsPointIn(PlayerPosition);
}

bool UPlaneArea::IsPlayerUnder()
{
	if (FMath::IsNearlyZero(DeathHeight)) return false;//未配置死亡深度
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())) return false;
	FVector PlayerPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	return PlayerPos.Z <= DeathHeight;

}

bool UPlaneArea::IsPlayerFlyCeiling()
{
	if (FMath::IsNearlyZero(FlyHeight)) return false;//未配置飞行深度
	if (!IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter())) return false;
	FVector PlayerPos = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()->GetActorLocation();
	return FlyHeight <= PlayerPos.Z;
}

void UPlaneArea::SetPolygon(const TArray<FVector>& wallPosList)
{
	VectPoly.Empty();
	for (auto pos : wallPosList)
	{
		VectPoly.Add(FVector2D(pos.X, pos.Y));
	}
}

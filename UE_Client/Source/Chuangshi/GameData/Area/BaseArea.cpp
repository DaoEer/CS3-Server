// Fill out your copyright notice in the Description page of Project Settings.

#include "BaseArea.h"
#include "Util/CS3Debug.h"
#include "Actor/ServerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"

UBaseArea::UBaseArea()
{
}

UBaseArea::~UBaseArea()
{
}

void UBaseArea::InitDatas(FAREA_DATA * AreaRow)
{
	UpdatePoint(AreaRow->Polygon);
	MapScriptID = AreaRow->MapScriptID;
	ScriptID = AreaRow->ScriptID;
	AreaName = AreaRow->AreaName;
	CeilHeight = AreaRow->CeilHeight;
	FloorHeight = AreaRow->FloorHeight;
}

void UBaseArea::UpdatePoint(TArray<FVector2D> Points)
{
	if (!PolyPtr.IsValid())
	{
		PolyPtr = TSharedPtr<Poly>(new Poly());
	}
	PolyPtr.Get()->UpdatePoints(Points);
}

bool UBaseArea::IsPointIn(FVector& Position)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UAreaBase IsPointIn  begin----------------------->>>"));
	if (!PolyPtr.IsValid())
	{
		return false;
	}
	// 如果所在高度不在范围内
	if (Position.Z<FloorHeight || Position.Z>CeilHeight)
	{
		return false;
	}
	return PolyPtr.Get()->IsPointIn(Position);
}

bool UBaseArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBaseArea::IsPlayerIn : PlayerActor!"));
		return false;
	}

	//获取当前Level
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (!level.Equals(MapScriptID))return false;

	FVector PlayerPosition = PlayerActor->GetActorLocation();
	return IsPointIn(PlayerPosition);
}

void UBaseArea::OnEnter(const FString SpaceScriptID)
{

}

void UBaseArea::OnLeave(const FString SpaceScriptID)
{

}
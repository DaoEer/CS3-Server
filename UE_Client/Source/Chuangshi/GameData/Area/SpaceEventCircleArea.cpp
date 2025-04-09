// Fill out your copyright notice in the Description page of Project Settings.

#include "SpaceEventCircleArea.h"
#include "Vector.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"



USpaceEventCircleArea::USpaceEventCircleArea()
{
}

USpaceEventCircleArea::~USpaceEventCircleArea()
{

}

void USpaceEventCircleArea::InitParams(FString _ScriptID, INT32 _EventType, INT32 _EventID, FString Param1, FString Param2, FString Param3)
{
	Supper::InitParams(_ScriptID,_EventType, _EventID, Param1, Param2, Param3);
	FString SplitStr = FString(TEXT("|"));
	TArray<FString> FSplitArray = UGolbalBPFunctionLibrary::SplitString(Param1, true, SplitStr);
	if (FSplitArray.Num()<2)
	{
		return;
	}
	CeilHeight = FSTRING_TO_FLOAT(FSplitArray[0]);
	FloorHeight = FSTRING_TO_FLOAT(FSplitArray[1]);

	FString SplitStr1 = FString(TEXT(" "));
	TArray<FString> FSplitArray1 = UGolbalBPFunctionLibrary::SplitString(Param2, true, SplitStr1);
	if (FSplitArray1.Num() < 3)
	{
		return;
	}
	Point = FVector(FSTRING_TO_FLOAT(FSplitArray1[0]), FSTRING_TO_FLOAT(FSplitArray1[1]), FSTRING_TO_FLOAT(FSplitArray1[2]));

	Range = FSTRING_TO_FLOAT(Param3) * 100;
}

bool USpaceEventCircleArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceEventCircleArea::IsPlayerIn : PlayerActor!"));
		return false;
	}


	FVector PlayerPosition = PlayerActor->GetActorLocation();
	
	if (PlayerPosition.Z<FloorHeight || PlayerPosition.Z>CeilHeight)
	{
		return false;
	}

	// 两个坐标点之间的距离
	int Distance = FVector::Dist(Point, PlayerPosition);
	if (Distance > Range)return false;

	return true;
}
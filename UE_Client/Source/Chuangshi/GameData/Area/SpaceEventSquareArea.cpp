// Fill out your copyright notice in the Description page of Project Settings.

#include "SpaceEventSquareArea.h"
#include "Vector.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"


USpaceEventSquareArea::USpaceEventSquareArea()
{
}

USpaceEventSquareArea::~USpaceEventSquareArea()
{

}

void USpaceEventSquareArea::InitParams(FString _ScriptID, INT32 _EventType, INT32 _EventID, FString Param1, FString Param2, FString Param3)
{
	Supper::InitParams(_ScriptID, _EventType, _EventID, Param1, Param2, Param3);
	FString SplitStr = FString(TEXT("|"));
	FString SplitStr1 = FString(TEXT(" "));

	TArray<FString> FSplitArray = UGolbalBPFunctionLibrary::SplitString(Param1, true, SplitStr);
	if (FSplitArray.Num() < 2)
	{
		return;
	}
	CeilHeight = FSTRING_TO_FLOAT(FSplitArray[0]);
	FloorHeight = FSTRING_TO_FLOAT(FSplitArray[1]);

	float X;
	float Y;
	FVector2D Point;
	TArray<FVector2D> Points;

	TArray<FString> FSplitArray1 = UGolbalBPFunctionLibrary::SplitString(Param2, true, SplitStr);
	for (auto Vector2DStr : FSplitArray1)
	{
		TArray<FString> FSplitArray2 = UGolbalBPFunctionLibrary::SplitString(Vector2DStr, false, SplitStr1);
		if (FSplitArray2.Num() >= 2)
		{
			X = FSTRING_TO_FLOAT(FSplitArray2[0]);
			Y = FSTRING_TO_FLOAT(FSplitArray2[1]);
			Point = FVector2D(X, Y);
			Points.Add(Point);
		}
		
	}
	UpdatePoint(Points);
	
}
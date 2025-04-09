// Fill out your copyright notice in the Description page of Project Settings.


#include "SpaceStagePolyArea.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"


USpaceStagePolyArea::USpaceStagePolyArea()
{
}

USpaceStagePolyArea::~USpaceStagePolyArea()
{
}

void USpaceStagePolyArea::InitParams(FString _ScriptID,INT32 _StageIndex, INT32 _TaskIndex, float _CeilHeight, float _FloorHeight, FString AreaParam)
{
	Supper::InitParams(_ScriptID, _StageIndex, _TaskIndex, _CeilHeight, _FloorHeight, AreaParam);
	FString SplitStr = FString(TEXT("|"));
	FString SplitStr1 = FString(TEXT(" "));

	float X;
	float Y;
	FVector2D Point;
	TArray<FVector2D> Points;

	TArray<FString> FSplitArray1 = UGolbalBPFunctionLibrary::SplitString(AreaParam, true, SplitStr);
	for (auto Vector2DStr : FSplitArray1)
	{
		TArray<FString> FSplitArray2 = UGolbalBPFunctionLibrary::SplitString(Vector2DStr, true, SplitStr1);
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


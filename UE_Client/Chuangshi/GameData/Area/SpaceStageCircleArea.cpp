// Fill out your copyright notice in the Description page of Project Settings.


#include "SpaceStageCircleArea.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "Actor/ServerCharacter.h"

USpaceStageCircleArea::USpaceStageCircleArea()
{
}

USpaceStageCircleArea::~USpaceStageCircleArea()
{
}

/**
@param AreaParam: 格式"x y z:range"
*/
void USpaceStageCircleArea::InitParams(FString _ScriptID, INT32 _StageIndex, INT32 _TaskIndex, float _CeilHeight, float _FloorHeight, FString AreaParam)
{
	Supper::InitParams(_ScriptID, _StageIndex, _TaskIndex, _CeilHeight, _FloorHeight, AreaParam);
	FString SplitStr = FString(TEXT(":"));
	FString SplitStr1 = FString(TEXT(" "));
	
	TArray<FString> FSplitArray = UGolbalBPFunctionLibrary::SplitString(AreaParam, true, SplitStr);
	if (FSplitArray.Num() > 1)
	{
		Range = FSTRING_TO_FLOAT(FSplitArray[1]) * 100;
	}
	else
	{
		CS3_Warning(TEXT("----USpaceStageCircleArea::InitParams------  AreaParam: (%s) missing Range,the format is 'x y z:range'"),*AreaParam);
	}
	
	TArray<FString> FSplitArray1 = UGolbalBPFunctionLibrary::SplitString(FSplitArray[0], true, SplitStr1);
	if (FSplitArray1.Num() > 2)
	{
		Point = FVector(FSTRING_TO_FLOAT(FSplitArray1[0]), FSTRING_TO_FLOAT(FSplitArray1[1]), FSTRING_TO_FLOAT(FSplitArray1[2]));
	}
	else
	{
		CS3_Warning(TEXT("----USpaceStageCircleArea::InitParams------   AreaParam: (%s) position format error,the format is 'x y z:range'"), *AreaParam);
	}
	
}

bool USpaceStageCircleArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceStageCircleArea::IsPlayerIn : PlayerActor!"));
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



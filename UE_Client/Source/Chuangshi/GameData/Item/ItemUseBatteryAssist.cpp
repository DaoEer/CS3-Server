// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemUseBatteryAssist.h"
#include "Util/GolbalBPFunctionLibrary.h"

FRotator UItemUseBatteryAssist::GetModelRotationAssist(const AServerCharacter * Owner)
{
	TArray<FString> SplitArr = UGolbalBPFunctionLibrary::SplitString(Param5, false, TEXT(" "));
	if (SplitArr.Num() >= 3)
	{
		return FRotator(FSTRING_TO_FLOAT(SplitArr[1]), FSTRING_TO_FLOAT(SplitArr[2]), FSTRING_TO_FLOAT(SplitArr[0]));
	}
	return FRotator::ZeroRotator;
}

bool UItemUseBatteryAssist::CheckModelAssistValid(const FVector & Pos)
{
	TArray<FString> strArr = UGolbalBPFunctionLibrary::SplitString(Param4, false, TEXT("|"));
	TArray<FVector> VectorArr;
	float Radius(10.0);
	for (auto strPos : strArr)
	{
		TArray<FString> SplitArr = UGolbalBPFunctionLibrary::SplitString(strPos, false, TEXT(" "));
		if (SplitArr.Num() >= 3)
		{
			VectorArr.Add(FVector(FSTRING_TO_FLOAT(SplitArr[0]), FSTRING_TO_FLOAT(SplitArr[1]), FSTRING_TO_FLOAT(SplitArr[2])));
		}
		else if (SplitArr.Num() == 1)
		{
			Radius = FSTRING_TO_FLOAT(SplitArr[0]);
		}

	}
	for (auto vPos : VectorArr)
	{
		if (FVector::Dist2D(Pos, vPos) <= Radius)
		{
			return true;
		}
	}
	return false;
}
// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemBattleFormations.h"
#include "Util/GolbalBPFunctionLibrary.h"


FString UItemBattleFormations::GetBattleFormationsHP()
{
	TArray<FString> strArr = UGolbalBPFunctionLibrary::SplitString(Param2);
	if (strArr.Num() >= 3)
	{
		return strArr[2];
	}
	return TEXT("");
}


void UItemBattleFormations::GetPerAndTotalSoume(int32 & PerSoume, int32 & TotalSoume)
{
	TArray<FString> strArr = UGolbalBPFunctionLibrary::SplitString(Param1);
	if (strArr.Num() >= 2)
	{
		TotalSoume = FSTRING_TO_INT(strArr[0]);
		PerSoume = FSTRING_TO_INT(strArr[1]);
	}
}

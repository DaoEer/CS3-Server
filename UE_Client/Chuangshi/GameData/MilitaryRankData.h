// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "MilitaryRankData.generated.h"

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FMilitaryRankData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///军功
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 exploit = 0;
	///军衔等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	///军衔称号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString title;
	///奖励兵力经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 exp = 0;
	///奖励兵力经验加成
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 expRate = 0;
	///解锁物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString itemGrade;
	///奖励物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString item;
	//点亮的图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "", DisplayName = "highLight")
		TSoftObjectPtr<UTexture2D> highLight;
	//不点亮的图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "", DisplayName = "UnHighLight")
		TSoftObjectPtr<UTexture2D> UnHighLight;

};
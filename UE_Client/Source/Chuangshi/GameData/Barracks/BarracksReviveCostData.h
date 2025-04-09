// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BarracksReviveCostData.generated.h"

/**
* 文件名称：BarracksReviveCostData.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-06-23
*/

USTRUCT(BlueprintType)
struct FBARRACKS_REVIVE_COST_ITEM_DATA
{
	GENERATED_BODY()
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
	int32 level;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "money")
	int32 money;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_REVIVE_COST_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ScriptID")
		FString scriptID;

	///花费金币
	UPROPERTY(EditAnywhere, BlueprintReadWrite,  DisplayName = "Cost")
		TArray<FBARRACKS_REVIVE_COST_ITEM_DATA> item;
};

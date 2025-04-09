// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "AreaMap.generated.h"

/**
* 文件名称：AreaMap.h
* 功能说明：地图区域数据
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-06
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FAREA_MAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///位面区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaMap", DisplayName = "PlaneArea")
		TArray<FString> PlaneArea;

	///子区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaMap", DisplayName = "SubArea")
		TArray<FString> SubArea;

	///复活区域
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaMap", DisplayName = "ReviveArea")
		TArray<FString> ReviveArea;
};

/**
*功能说明：地图区域限制：位面和副本
*创建时间：2018.4.13
*文件作者：zhangfudong
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAREA_TERRAINCLASSIFICATION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///地图名称 + 阶段编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaWall", DisplayName = "Name")
		FString Name;

	///数据点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "AreaWall", DisplayName = "Position")
		TArray<FVector> Position;
};
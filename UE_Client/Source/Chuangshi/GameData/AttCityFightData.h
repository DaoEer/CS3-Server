// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "CsvTableRowBase.h"
#include "AttCityFightData.generated.h"

/**
* 文件名称：AttCityFightData.h
* 功能说明：攻城战数据相关
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-01-10
*/

/** 攻城梯结构体 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FATT_CITY_LADDER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//攻城梯唯一ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AttCityFightData")
		FString Id;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AttCityFightData")
		FVector Location;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AttCityFightData")
		FRotator Rotation;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AttCityFightData")
		FVector Scale;
	//模型ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AttCityFightData")
		FString ModelNumber;
};
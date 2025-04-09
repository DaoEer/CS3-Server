// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BloodData.generated.h"
/**
* 文件名称：BloodData.h
* 功能说明：血条数量
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-7-9
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBloodData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "BloodNum")
		int32 BloodNum = 0;

};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "StallData.generated.h"
/**
* 文件名称：StallData.h
* 功能说明：摆摊寻路点
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-7-12
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FStallPointData
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "id")
		int32 id = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "position")
		FVector position;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "direction")
		FVector direction;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FStallData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "StallPoint")
		TArray<FStallPointData> StallPoint;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		if (this->StallPoint.Num() == 0)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("The value of StallPoint is empty!\n"));
		}
		else
		{
			ResultInfo.Result = Ok;
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};
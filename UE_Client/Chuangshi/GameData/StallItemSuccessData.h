// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "StallItemSuccessData.generated.h"

/**
* 文件名称：StallRecordData.h
* 功能说明：摆摊记录数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-04-21
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FStallItemSuccessData
{
	GENERATED_USTRUCT_BODY()
		FStallItemSuccessData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StallName")
		FString StallName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemName")
		FString ItemName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TotalPrice")
		int32 TotalPrice = 0;
};


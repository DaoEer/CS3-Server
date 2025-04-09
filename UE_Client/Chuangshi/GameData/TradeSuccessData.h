// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "TradeSuccessData.generated.h"

/**
* 文件名称：TradeSuccessData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-4-19
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTradeSuccessData
{
	GENERATED_USTRUCT_BODY()
		FTradeSuccessData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Uid")
		FString Uid;
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Price")
		int32 Price = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TotalPrice")
		int32 TotalPrice = 0;
};

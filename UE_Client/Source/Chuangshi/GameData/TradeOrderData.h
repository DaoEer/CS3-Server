// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "TradeOrderData.generated.h"

/**
* 文件名称：TradeOrderData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-04-19
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTradeOrderData
{
	GENERATED_USTRUCT_BODY()
		FTradeOrderData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Uid")
		FString Uid;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RemainTime")
		int64 RemainTime;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Price")
		int32 Price = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TradeType")
		int32 TradeType = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EarnMoney")
		int32 EarnMoney = 0;
	bool operator ==(const FTradeOrderData& other)
	{
		if (other.Uid == Uid)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

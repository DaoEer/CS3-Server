// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GiftGoodsData.generated.h"

/**
* 文件名称：GiftGoodsData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-04-07
*/

UENUM(BlueprintType)
enum class GIFTSTATE : uint8
{
	GIFT_STATE_WAIT = 0	UMETA(DisplayName = "GIFT_STATE_WAIT"),
	GIFT_STATE_OVERRDUE = 1   UMETA(DisplayName = "GIFT_STATE_OVERRDUE"),
	GIFT_STATE_RECEIVE = 2	UMETA(DisplayName = "GIFT_STATE_RECEIVE"),
	GIFT_STATE_WITHDRAW = 3	UMETA(DisplayName = "GIFT_STATE_WITHDRAW"),
	GIFT_STATE_REFUSE = 4	UMETA(DisplayName = "GIFT_STATE_REFUSE"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FGiftGoodsData
{
	GENERATED_USTRUCT_BODY()
		FGiftGoodsData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "GoodsDataUID")
		FString GoodsDataUID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemName")
		FString ItemName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Time")
		int64 Time;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PlayerName")
		FString PlayerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "State")
		GIFTSTATE State = GIFTSTATE::GIFT_STATE_WAIT;
	bool operator ==(const FGiftGoodsData& other)
	{
		if (other.GoodsDataUID == GoodsDataUID)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

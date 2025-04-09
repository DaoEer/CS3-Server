#pragma once
#include "CoreMinimal.h"
#include "BuyShopMallItemData.generated.h"

/**
* 文件名称：BuyShopMallItemData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-04-07
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBuyShopMallItemData
{
	GENERATED_USTRUCT_BODY()
		FBuyShopMallItemData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ShopMallType")
	FString ShopMallType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Slot")
	FString Slot;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MoneyType")
		int32 MoneyType = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemType")
		int32 ItemType = 0;
};
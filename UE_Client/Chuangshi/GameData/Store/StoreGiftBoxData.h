#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "StoreGiftBoxData.generated.h"

/**
* 文件名称：StoreGiftBoxData.h
* 功能说明：商城礼品盒数据结构
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-05-08
*/

/** 商城礼品盒数据结构 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_GIFT_BOX : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "goodsID")
		int32 goodsID = 0;
	///数量
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "amount")
		int32 amount = 0;
	///收礼者名字
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "receiverName")
		FString receiverName;
	///收礼者DBID
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "receiverDBID")
		FString receiverDBID;
	///赠礼者名字
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "senderName")
		FString senderName;
	///赠礼者DBID
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "senderDBID")
		FString senderDBID;
	///删除时间
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "endTime")
		FString endTime;
	///礼品状态
	///0 礼品默认状态
	///1 已过期
	///2 对方已接受
	///3 对方已拒绝
	///4 已取回
	///5 已接受
	///6 已拒绝
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "giftState")
		int32 giftState;
	///留言
	UPROPERTY( BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "Message")
		FString message;
	///uid
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "uid")
		FString uid;
	///过期时间
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "overtime")
		FString overtime;
	///总价
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "price")
		int32 price;
	///物品ID
	UPROPERTY(BlueprintReadOnly, Category = "FSTORE_GIFT_BOX", DisplayName = "itemID")
		int32 itemID;
};
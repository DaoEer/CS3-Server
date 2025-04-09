#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "StoreRecordData.generated.h"

/**
* 文件名称：StoreRecordData.h
* 功能说明：商城记录
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-04-22
*/

/** 购买记录数据 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_BUY_RECORD_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "goodsID")
		int32 goodsID = 0;
	///数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "amount")
		int32 amount = 0;
	///购买时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "buyTime")
		FString buyTime;
	///uid
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "uid")
		FString uid;
	///花费
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "price")
		int32 price;
	///商品类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "goodsType")
		int32 goodsType;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_BUY_RECORD_DATA", DisplayName = "itemID")
		int32 itemID;
};

/** 赠送记录数据 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTORE_PRESENT_RECORD_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "goodsID")
		int32 goodsID = 0;
	///数量
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "amount")
		int32 amount = 0;
	///购买时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "buyTime")
		FString buyTime;
	///uid
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "uid")
		FString uid;
	///送礼人名字
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "sender")
		FString sender;
	///收礼人名字
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "receiver")
		FString receiver;
	///花费
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "price")
		int32 price;
	///收礼人DBID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "receiverDBID")
		FString receiverDBID;
	///赠礼人名字DBID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "senderDBID")
		FString senderDBID;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FSTORE_PRESENT_RECORD_DATA", DisplayName = "itemID")
		int32 itemID;
};
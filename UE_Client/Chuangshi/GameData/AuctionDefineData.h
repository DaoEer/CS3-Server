#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "AuctionDefineData.generated.h"

/**
* 文件名称：AuctionDefineData.h
* 功能说明：竞拍分配数据类定义
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-11-26
*/

///竞拍信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAUCTIONMESSAGE
{
	GENERATED_USTRUCT_BODY()
public:
	///玩家dbid
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayerDBID;
	///玩家出价金额（0表示放弃）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BidMoney;
};

///竞拍
UCLASS(BlueprintType)
class CHUANGSHI_API UAuctionData : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 宝箱id
	UPROPERTY(BlueprintReadOnly)
		int32 dropboxID;

	///< 物品uid
	UPROPERTY(BlueprintReadOnly)
		FString uid;

	///< 所有者dbid（出价最高且获得了该物品的玩家）默认为0
	UPROPERTY(BlueprintReadOnly)
		FString ownerDBID;

	///< 物品是否已分配（0：否 1：是）
	UPROPERTY(BlueprintReadOnly)
		uint8 isPickUp;

	///< 当前出价最高的玩家dbid 默认为0
	UPROPERTY(BlueprintReadOnly)
		FString maxAuctionDBID;

	///< 当前最高出价 默认为-1
	UPROPERTY(BlueprintReadOnly)
		int32 maxAuctionMoney;

	///< 当前自身出价 -1：还未出价 0：放弃竞拍 默认为-1
	UPROPERTY(BlueprintReadOnly)
		int32 selfMoney;

	///< 竞拍轮数 默认第0轮 (最低出价为底价)
	UPROPERTY(BlueprintReadOnly)
		int32 round;

	///< 当前参与竞拍的人数 默认为0
	UPROPERTY(BlueprintReadOnly)
		int32 curAuctionRoleAmount;

	///< 竞拍消息数据 [[dbid, money], [dbid, money] ...]
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FAUCTIONMESSAGE> auctionMessageData;
};

///竞拍历史数据
UCLASS(BlueprintType)
class CHUANGSHI_API UAuctionHistroy : public UCS3Object
{
	GENERATED_BODY()
public:
	///< 物品id
	UPROPERTY(BlueprintReadOnly)
		FString id;

	///< 成交价
	UPROPERTY(BlueprintReadOnly)
		int32 money;

	///< 买家
	UPROPERTY(BlueprintReadOnly)
		FString roleName;

	///< 竞拍结果（0：失败 1：成功）
	UPROPERTY(BlueprintReadOnly)
		int32 result;
};
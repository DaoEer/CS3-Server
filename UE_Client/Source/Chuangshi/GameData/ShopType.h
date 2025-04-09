#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "ShopType.generated.h"

/**
* 文件名称：ShopType.h
* 功能说明：
* 文件作者：yikun
* 目前维护：chendongyong
* 创建时间：2018-04-10
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSHOP_TYPE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///商店名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShopName;
	///商店描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShopDescribe;
	///商店是否可回购
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCanbuyBack;
	///商店是否可修理
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCanRepair;
	///商店是否可出售
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCanSell;
	///商店是否可打折（根据帮会的铁匠铺）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsTongDisCount;
};


/// 战魂商店
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOMBAT_SOUL_SHOP_TYPE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///物品id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ItemID = 0;
	///左上角类型提示（如：外攻）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Type;
	///前置物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PreItemID = 0;
	///下一级物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 NextItemID = 0;
	///购买价格
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BuyPrice = 0;
	///出售价格
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SellPrice = 0;
	///提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Tip;
};

/// 魂卫商店
USTRUCT(BlueprintType)
struct CHUANGSHI_API FGUARD_SOUL_SHOP_TYPE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///魂卫scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString scriptID;
	///阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 camp = 0;
	///左上角类型提示（如：远程兵种）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString type;
	///魂卫名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString guardName;
	///最高购买次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 maxBuyTime = 0;
	///卡牌贴图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString carPath;
	///消耗（等级对应消耗，等级：消耗|等级：消耗....）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString buyPrice;
	///时间对应等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString levelRelevant;
	///提示1
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString tip_1;
	///提示2
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString tip_2;
};

/// 魂塔商店
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPAGODA_SOUL_SHOP_TYPE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///塔建筑scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString scriptID;
	///阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 camp = 0;
	///类型
	///	0：上路
	///	1：中路
	///	2：下路
	///	3：基地
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 type = 0;
	/// 等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	/// 是否还存活
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bSruvival = true;
	///熔岩塔scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lavaPagoda;
	///熔岩塔消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 lavaPrice = 0;
	///熔岩塔提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lavaTip;
	///冰封塔scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString icePagoda;
	///冰封塔消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 icePrice = 0;
	///冰封塔提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString iceTip;
	///陷地塔scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString trapPagoda;
	///陷地塔消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 trapPrice = 0;
	///陷地塔提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString trapTip;
	///玄灵塔scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString spiritPagoda;
	///玄灵塔消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 spiritPrice = 0;
	///玄灵塔提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString spiritTip;
};

/// 药品商店
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDRUG_SOUL_SHOP_TYPE_DATA
{
	GENERATED_BODY()
public:
	/// 物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 id;
	/// 购买价钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 buyPrice;
	/// 出售价钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 sellPrice;
};
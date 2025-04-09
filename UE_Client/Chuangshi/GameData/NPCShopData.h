// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "NPCShopData.generated.h"

/**
* 文件名称：NPCShopData.h
* 功能说明：
* 文件作者：huangshijie
* 目前维护：chendongyong
* 创建时间：2016-11-16
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNPCShopData : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()
		FNPCShopData() {};
public:
	///商店ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "shopID")
		FString shopID;
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Id")
		FString Id;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID = 0;
	///物品数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount = 0;
	///物品价格
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Price")
		FString Price;
	///刷新类型（缺省0）
	///	0：不刷新
	///	1：每周刷新
	///	2：每日刷新
	///	3：售完刷新
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RefreshType")
		int32 RefreshType = 0;
	///购买条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Condition")
		FString Condition;
	///限制购买次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "BuyLimit")
		int32 BuyLimit = 0;
	///是否共享（指的是数量是否共享）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsShared")
		bool IsShared = false;
	///分页标签
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Paging")
		FString Paging;
	///分页序号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PageIndex")
		int32 PageIndex = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongPlunderShopData
{
	GENERATED_USTRUCT_BODY()
public:
	///商品ID
	UPROPERTY(BlueprintReadOnly)
		FString ID;
	///物品ID
	UPROPERTY(BlueprintReadOnly)
		int32 ItemID = 0;
	///物品数量
	UPROPERTY(BlueprintReadOnly)
		int32 Amount;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBuyBackItemData
{
	GENERATED_BODY()
public:
	///物品ID
	UPROPERTY(BlueprintReadOnly)
		int32 Id;
	///物品Uid
	UPROPERTY(BlueprintReadOnly)
		FString Uid;
	///物品数量
	UPROPERTY(BlueprintReadOnly)
		int32 Amount = 0;
	///绑定类型
	UPROPERTY(BlueprintReadOnly)
		int32 BindType = 0;
	///物品战力
	UPROPERTY(BlueprintReadOnly)
		int32 CombatPower = 0;
	///基础属性
	UPROPERTY(BlueprintReadOnly)
		FString AttackPropertiesStr;
	///附加属性
	UPROPERTY(BlueprintReadOnly)
		FString AttachPropertiesStr;
	///强化属性
	UPROPERTY(BlueprintReadOnly)
		FString IntensifyDataStr;
	///耐久度
	UPROPERTY(BlueprintReadOnly)
		int32 Hardiness = 0;
};

/// 轮回秘境商店刷新消耗
USTRUCT(BlueprintType)
struct CHUANGSHI_API FLHMJShopReflashCostData : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()
		FLHMJShopReflashCostData() {};
public:
	/// 刷新次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "reflashNum")
		int32 reflashNum;
	/// 消耗金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "money")
		int32 money;
};

//随机限量商品配置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FNPCRandomLimitShopData : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()
		FNPCRandomLimitShopData() {};
public:
	///商店ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "shopID")
		FString shopID;
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Id")
		FString Id;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID = 0;
	///物品价格
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Price")
		FString Price;
	///购买条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Condition")
		FString Condition;
	///限制购买次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "BuyLimit")
		int32 BuyLimit = 0;
	///分页标签
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Paging")
		FString Paging;
	///分页序号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PageIndex")
		int32 PageIndex = 0;
	///刷新类型（缺省0）
	///	0：不刷新
	///	1：每周刷新
	///	2：每日刷新
	///	3：售完刷新
	/// 4：固定时间内刷新一次 
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RefreshType")
		int32 RefreshType = 0;
	///是否共享（指的是数量是否共享）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsShared")
		bool IsShared = false;
};

/// 神秘商人商品配置
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMysteriousShopData : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()
		FMysteriousShopData() {};
public:
	///商品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "id")
		int32 id;
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "itemID")
		int32 itemID = 0;
	///物品价格（数据格式跟NPC商店一样）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "price")
		FString price; 
	///限制购买次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "buyLimit")
		int32 BuyLimit = 0;
	///概率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "probability")
		float probability;
	///位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "slotID")
		int32 slotID;
};
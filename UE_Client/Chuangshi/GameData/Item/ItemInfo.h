// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "ItemInfo.generated.h"

/**
* 文件名称：ItemInfo.h
* 功能说明：物品部分动态数据
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-11
*/

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FItemPartInfo
{
	GENERATED_USTRUCT_BODY()
public:
	//物品ItemID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemInfo")
		int32 ItemID = 0;
	//物品的位置（绝对位置）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemInfo")
		int32 ItemOrder = 0;
	//物品Amount
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemInfo")
		int32 Amount = 0;
	//物品绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemInfo")
		int32 BindType = 0;
	//物品UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemInfo")
		FString UID;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FItemTypeInfo : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemType")
	FString ItemType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ShopMallItemType")
	FString ShopMallItemType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPCShopItemType")
	FString NPCShopItemType;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "StallItemType")
	FString StallItemType;

	///能否拖拽到快捷栏
	///	0：不可拖
	///	1：可拖
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 CanDragToQB;

};
USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FItemUseAmountInfo
{
	GENERATED_USTRUCT_BODY()
public:
	//物品ItemID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemUseAmountInfo")
	int32 ItemID = 0;
	//物品使用限量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemUseAmountInfo")
	int32 ItemUseAmount = 0;
	//物品最后使用时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemUseAmountInfo")
	FString ItemCreateTime;
};
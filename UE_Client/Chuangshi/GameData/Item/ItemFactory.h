// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/Equip.h"
#include "GameData/Item/CS3ItemData.h"
#include "Manager/ResourceManager.h"
#include "ItemFactory.generated.h"

/**
* 文件名称：ItemFactory.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-17
*/


// 装备部件
UENUM(BlueprintType)
enum class EQUIP_TYPE :uint8
{
	// 无
	EQUIP_TYPE_NONE = 0,
	// 武器
	EQUIP_TYPE_WEAPON = 1,
	// 防具
	EQUIP_TYPE_ARMOR = 2,
	// 饰品
	EQUIP_TYPE_JEWELRY = 3,
};


UCLASS(BlueprintType)
class CHUANGSHI_API UItemFactory : public UCS3Object
{
	GENERATED_BODY()
public:

	static UItemFactory* GetInstance();
	/**
	*BlueprintCallable，通过物品ID获取物品数据
	*动态创建一个ItemBase
	*如果只是想获取物品配置表里的数据，请用GetStaticDataByItemID
	*
	*@param itemid 物品ID
	*
	*@return UItemBase* 物品数据
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemFactory")
		static UItemBase* GetItemByID(int32 itemid);

	/**
	*BlueprintPure，通过物品ID获取物品配置数据
	*
	*@param itemid 物品ID
	*
	*@return FCS3ItemData 物品配置数据
	*/
	UFUNCTION(BlueprintPure, Category = "ItemFactory")
		static const FCS3ItemData GetStaticDataByItemID(int32 itemid);
	
	/**
	*BlueprintPure，通过物品ID获取物品图标路径
	*
	*@param itemid 物品ID
	*
	*@return FString 物品图标路径
	*/
	UFUNCTION(BlueprintPure, Category = "ItemFactory")
		static FString GetIconPath(int32 itemid);	

	// 获取装备部件（如果不是装备，返回EQUIP_TYPE::EQUIP_TYPE_NONE）
	UFUNCTION(BlueprintPure, Category = "ItemFactory")
		EQUIP_TYPE GetEquipType(int32 itemid);

	//异步加载物品ICON资源
	UFUNCTION(BlueprintCallable, Category = "ItemFactory")
		static void AsyncLoadItemIconAsset(FResourceLoaderIconDelegate DelegateToCall, int32 itemid, FString ItemIcon);

	//复制物品Tips相关的基础信息到另一个物品
	UFUNCTION(BlueprintCallable, Category = "ItemFactory")
		static void ItemTipsInfoCopy(UItemBase* SrcItem, UItemBase* DstItem);

	//复制装备Tips相关的基础信息到另一个装备
	UFUNCTION(BlueprintCallable, Category = "ItemFactory")
		static void EquipTipsInfoCopy(UEquip* SrcItem, UEquip* DstItem);

	/**
private:
	static UItemFactory* Instance;*/
};

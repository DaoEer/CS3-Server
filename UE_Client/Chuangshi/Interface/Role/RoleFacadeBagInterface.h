// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Item/ItemBase.h"
#include "RoleFacadeBagInterface.generated.h"

/*
* 文件名称：RoleFacadeBagInterface.h
* 功能说明：玩家外观背包
* 文件作者：yikun
* 目前维护：chendongyong
* 创建时间：2017-08-05
*/

UENUM(BlueprintType)
enum class FACADEITEMTYPE : uint8
{
	ITEM_CHENGYI = 1	UMETA(DisplayName = "ITEM_CHENGYI"), ///<成衣
	ITEM_WAIZHUANG = 2	UMETA(DisplayName = "ITEM_WAIZHUANG"),///<外装
	ITEM_FACE = 3   UMETA(DisplayName = "ITEM_FACE"),		///<易容
	ITEM_PENDANT = 4	UMETA(DisplayName = "ITEM_PENDANT"),///<挂件
	ITEM_DECORATION = 5	UMETA(DisplayName = "ITEM_DECORATION"),///<装饰
};
UCLASS(BlueprintType)
class CHUANGSHI_API URoleFacadeBagInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleFacadeBagInterface();
	~URoleFacadeBagInterface();
	static FString GetName() { return TEXT("RoleFacadeBagInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.RoleFacadeBagInterface'"); } //获取蓝图对象路径
		

	///**
	//*接收外观背包物品数据
	//*
	//*@param data 物品数据
	//*
	//*@return 无
	//*/
	//UFUNCTION(BlueprintCallable, Category = "RoleFacadeBagInterface")
	//	void ReceiveFacadeBagItem(const FString& data);

	/**
	*获取物品信息
	*
	*@param jsonstr 物品信息
	*@param itemid 物品id
	*@param itemorder 物品位置
	*@param amount 物品数量
	*@param bindtype 绑定类型
	*@param uid 物品UID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Server")
		void GetItemInfoByString(const FString& jsonstr, int32& itemid, int32& itemorder, int32& amount, int32& bindtype, FString& uid, int32& itemType);

	virtual void InitBlueCB() override;
public:
	TMap<int32, TMap<FString, UItemBase*>> FFB_ItemList;
};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Interface/NPCBaseObjectInterface.h"
#include "GameData/Item/ItemBase.h"
#include "DropBoxInterface.generated.h"

/*
* 文件名称：DropBoxInterface.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-07-29
*/

/**
 * 掉落物品接口类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UDropBoxInterface : public UNPCBaseObjectInterface
{
	GENERATED_BODY()
	typedef UNPCBaseObjectInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	UDropBoxInterface();
	~UDropBoxInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.DropBoxInterface'"); } //获取蓝图对象路径
	virtual void InitBlueCB() override;

	///< 清空拾取物品Item列表（关闭拾取界面的时候会关闭宝箱并清空该列表）
	UFUNCTION(BlueprintCallable, Category = "DropBoxInterface")
		void ClearPickUpItemList();

	///< 判断UID在不在拾取物品列表里面
	UFUNCTION(BlueprintCallable, Category = "DropBoxInterface")
		bool HasUIdInItemList(const FString& UId);

	///<更新拾取物品信息列表（UId：拾取物品的UID，LeftAmount：拾取过后宝箱剩余某个物品数量）
	void UpdateItemList(const FString& UId, int32 LeftAmount);

public:
	///<正在进行掷骰子的物品Uid列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "DropBoxInterface")
		TArray<UItemBase*> FPK_ItemList;
};

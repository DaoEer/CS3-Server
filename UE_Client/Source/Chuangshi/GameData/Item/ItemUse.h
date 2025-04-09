// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Item/ItemBase.h"
#include "ItemUse.generated.h"

/**
* 文件名称：ItemUse.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-17
*/


class AServerCharacter;

/**
 * 物品使用类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UItemUse : public UItemBase
{
	GENERATED_BODY()
	
public:
	virtual void BeginDestroy()override;
	/**
	*BlueprintCallable，使用物品
	*
	*@param player 玩家
	*
	*@return int32 使用结果
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemUse | Use")
		virtual int32 Use(AServerCharacter* player);

	/**
	*BlueprintCallable，查询使用结果
	*
	*@param player 玩家
	*
	*@return int32 使用结果
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemUse | Use")
		virtual int32 UseQuery(AServerCharacter* player);

	UFUNCTION(BlueprintCallable, Category = "ItemUse | Use")
		void NotityUseItemToCell();///<BlueprintCallable，通知服务器调用useItem方法

	/**
	*BlueprintCallable，检测物品是否正在使用
	*
	*@return bool 当前正在使用返回true，否则为false
	*/
	//UFUNCTION(BlueprintCallable, Category = "ItemBase")
	virtual bool IsUsing() override;

	/**
	*虚函数，是否可以使用物品
	*
	*@return bool 可以使用物品返回TRUE，否则返回FALSE
	*/
	virtual bool IsCanUse() override;

	/**
	*BlueprintCallable，判断物品是否在使用CD中
	*
	*@return bool 在使用CD返回true，否则为false
	*/
	virtual	bool IsCoolDowning() override;

	/**
	* 启动CD计时器
	*
	*@param TimeRemaining CD时间
	*
	*@return 无
	*/
	void StartCdTime(float TimeRemaining);

	void StopCdTime();///<停止CD计时器
	
	/**
	*BlueprintCallable，获取物品在CD中的剩余CD时间
	*
	*@return float 物品使用CD中，剩余CD时间
	*/
	virtual float GetCDRemainningTime() override;

	virtual void SetCDPersistTime(float PersistTime) override;

	virtual float GetCDPersistTime() override;

	virtual bool IsUseItemToPosition();
	virtual void UseItemToPosition();
	virtual void SetUseItemToPositionBeforeNotifyServer(); ///<使用对位置释放的物品前的调用(没有到服务器) 具体需求可见JIRA CST-6736
	virtual void CancelUseItemToPositionBeforeNotifyServer();///<取消使用对位置释放的物品前的调用或者通知服务器前调用(没有到服务器)
protected:
	UPROPERTY()
		FTimerHandle CdTimerHandle;///<CD计时器
	
	UPROPERTY()
		float CDPersistTime;   ///CD持续总时间
};

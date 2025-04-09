// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "ReviveArea.generated.h"

/**
* 文件名称：ReviveArea.h
* 功能说明：地图复活区域
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-1-17
*/

/**
* 地图复活区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UReviveArea : public UBaseArea
{
	GENERATED_BODY()

public:
	UReviveArea();
	~UReviveArea();

	/**
	*初始化区域数据
	*
	*@param AreaRow 区域数据
	*
	*@return 无
	*/
	void InitDatas(FAREA_DATA* AreaRow);

	/**
	*玩家是否在死亡高度以下
	*
	*@return bool 玩家在死亡高度以下返回TRUE，否则返回FALSE
	*/
	bool IsPlayerUnder();

public:	
	///死亡高度
	float DeathHeight;
	///复活地图
	FString ReviveSpace;
	///复活位置
	FVector RevivePosition;
	///复活朝向
	FRotator ReviveDirection;
};
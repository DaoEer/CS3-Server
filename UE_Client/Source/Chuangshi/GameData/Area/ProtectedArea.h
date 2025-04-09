// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "ProtectedArea.generated.h"

/**
* 文件名称：ProtectedArea.h
* 功能说明：保护区域（在死亡高度下时，触发传送到固定位置，而不是死亡）
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2018-12-25
*/

/**
* 保护区域（在死亡高度下时，触发传送到固定位置，而不是死亡）
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UProtectedArea : public UBaseArea
{
	GENERATED_BODY()
	
public:
	UProtectedArea();
	~UProtectedArea();

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

	/**
	*在死亡高度下触发传送到目标区域
	*
	*@return 无
	*/
	void Triger();


private:
	///死亡高度
	float DeathHeight;
	///复活地图
	FString ReviveSpace;
	///复活位置
	FVector RevivePosition;
	///复活朝向
	FRotator ReviveDirection;
};

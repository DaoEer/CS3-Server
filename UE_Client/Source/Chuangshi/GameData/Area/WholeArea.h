// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "WholeArea.generated.h"

/**
* 文件名称：WholeArea.h
* 功能说明：关卡区域
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-28
*/

/**
* 关卡区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UWholeArea : public UBaseArea
{
	GENERATED_BODY()

public:
	UWholeArea();
	~UWholeArea();
	/**
	*初始化区域数据
	*
	*@param AreaRow 区域数据
	*
	*@return 无
	*/
	void InitDatas(FAREA_DATA* AreaRow);

	/**
	*判断参数位置是否在区域范围内
	*
	*@param Position 位置
	*
	*@return bool 参数位置在区域范围内返回true，否则为false
	*/
	bool IsPointIn(FVector& Position) override;

	/**
	*玩家是否在死亡高度以下
	*
	*@return bool 玩家在死亡高度以下返回TRUE，否则返回FALSE
	*/
	bool IsPlayerUnder();

	/**
	*玩家是否在飞行高度以上
	*
	*@return bool
	*/
	bool IsPlayerFlyCeiling();

	/**
	*进入SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	void OnEnter(const FString SpaceScriptID)override;

	virtual SPACE_AREA_TYPE GetType() override { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_WHOLE; };

public:	
	float DeathHeight;///< 死亡高度
	float FlyHeight;///< 飞行高度
};

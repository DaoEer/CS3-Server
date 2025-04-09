// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "PlaneArea.generated.h"

/**
* 文件名称：PlaneArea.h
* 功能说明：位面区域
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2016-11-26
*/

/**
* 位面区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UPlaneArea : public UBaseArea
{
	GENERATED_BODY()

public:
	UPlaneArea();
	~UPlaneArea();

	/**
	*初始化位面数据
	*
	*@param AreaRow 位面数据
	*
	*@return 无
	*/
	void InitDatas(FAREA_DATA* AreaRow);

	/**
	*触发进入位面
	*
	*@param SpaceScriptID 位面ScriptID
	*
	*@return 无
	*/
	void trriger(const FString SpaceScriptID);

	/**
	*进入SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	void OnEnter(const FString SpaceScriptID) override;

	/**
	*玩家是否在位面附近Distance范围内
	*
	*@param Distance 位面附近范围
	*
	*@return bool 玩家在位面附近Distance范围内返回TRUE，否则返回FALSE
	*/
	bool IsPlayerCloseTo(float Distance);

	/**
	*判断当前Player是否在区域范围内
	*
	*@return bool 当前Player在区域范围内返回true，否则为false
	*/
	virtual bool IsPlayerIn() override;

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
	*获取多边形顶点数据
	*
	*@return TArray<FVector2D> 多边形顶点数据
	*/
	TArray<FVector2D> GetPolygon() { return VectPoly; }

	void SetPolygon(const TArray<FVector>& wallPosList);

	virtual SPACE_AREA_TYPE GetType() override { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_PLANE; }

	/**
	*获取是否上锁
	*
	*@return bool 上锁返回TRUE，否则FALSE
	*/
	bool IsLock() { return _IsLock; }

	/**
	*设置上锁状态
	*
	*@param Lock 是否上锁
	*
	*@return 无
	*/
	void IsLock(bool Lock) { _IsLock = Lock; }

public:
	float DeathHeight;///< 死亡高度
	float FlyHeight;///<飞行高度
private:
	TArray<FVector2D> VectPoly;///<多边形顶点坐标
	bool _IsLock = false;///<是否上锁
};

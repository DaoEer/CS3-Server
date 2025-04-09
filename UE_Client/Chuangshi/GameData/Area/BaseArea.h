// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Area.h"
#include "GameData/GameDeFine.h"
#include "Poly.h"
#include "BaseArea.generated.h"

/**
* 文件名称：BaseArea.h
* 功能说明：地图区域基类
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2016-11-26
*/

/**
* 地图区域基类
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UBaseArea : public UCS3Object
{
	GENERATED_BODY()

public:
	UBaseArea();
	~UBaseArea();

	/**
	*更新多边形PolyPtr的数据
	*
	*@param Points 多边形PolyPtr数据
	*
	*@return 无
	*/
	void UpdatePoint(TArray<FVector2D> Points);

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
	virtual bool IsPointIn(FVector& Position);

	/**
	*判断当前Player是否在区域范围内
	*
	*@return bool 当前Player在区域范围内返回true，否则为false
	*/
	virtual bool IsPlayerIn();

	/**
	*进入SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	virtual void OnEnter(const FString SpaceScriptID);

	/**
	*离开SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	virtual void OnLeave(const FString SpaceScriptID);

	virtual SPACE_AREA_TYPE GetType() { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_NONE; };

public:
	FString ScriptID;///< 地图ScriptID
	FString AreaName;///<区域名称
	FString MapScriptID;///< 映射的大地图

protected:
	TSharedPtr<Poly> PolyPtr = MakeShareable(new Poly());///< 多边形
	float CeilHeight;	///< 天空高度
	float FloorHeight;///< 地面高度
};
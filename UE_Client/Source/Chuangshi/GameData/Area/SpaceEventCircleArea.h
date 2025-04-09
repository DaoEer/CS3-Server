// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "UObject/NoExportTypes.h"
#include "GameData/Area/SpaceEventBaseArea.h"
#include "SpaceEventCircleArea.generated.h"

/**
* 文件名称：SpaceEventCircleArea.h
* 功能说明：进入某区域触发副本剧情事件，圆形区域
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-2-20
*/

/**
* 触发副本剧情事件的圆形区域
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceEventCircleArea : public USpaceEventBaseArea
{
	GENERATED_BODY()
		typedef USpaceEventBaseArea Supper;

public:
	USpaceEventCircleArea();
	~USpaceEventCircleArea();

	/**
	*初始化触发副本剧情事件的圆形区域数据
	*
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 天空高度和地面高度
	*@param Param2 圆心坐标2
	*@param Param3 半径
	*
	*@return 无
	*/
	void InitParams(FString ScriptID, INT32 EventType, INT32 EventID, FString Param1, FString Param2, FString Param3) override;

	/**
	*判断当前Player是否在区域范围内
	*
	*@return bool 当前Player在区域范围内返回true，否则为false
	*/
	bool IsPlayerIn() override;
protected:

	FVector Point;///<中心点
	float Range;	///< 半径
};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "GameData/CS3Object.h"
#include "UObject/NoExportTypes.h"
#include "GameData/Area/SpaceEventBaseArea.h"
#include "SpaceEventSquareArea.generated.h"

/**
* 文件名称：SpaceEventSquareArea.h
* 功能说明：进入某区域触发副本剧情事件，多边形区域
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-2-20
*/
/**
* 触发副本剧情事件的多边形区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceEventSquareArea : public USpaceEventBaseArea
{
	GENERATED_BODY()
		typedef USpaceEventBaseArea Supper;

public:
	USpaceEventSquareArea();
	~USpaceEventSquareArea();

	/**
	*初始化触发副本剧情事件的多边形区域类数据
	*
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 天空高度和地面高度
	*@param Param2 坐标位置
	*@param Param3 事件参数3
	*
	*@return 无
	*/
	void InitParams(FString ScriptID, INT32 EventType, INT32 EventID, FString Param1, FString Param2, FString Param3) override;
};
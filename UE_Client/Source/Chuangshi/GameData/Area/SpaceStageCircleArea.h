// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/SpaceStageBaseArea.h"
#include "SpaceStageCircleArea.generated.h"

/**
* 文件名称：SpaceStageCircleArea.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-03-01
*/

/**
 * 触发副本阶段目标完成的圆形区域类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceStageCircleArea : public USpaceStageBaseArea
{
	GENERATED_BODY()
		typedef USpaceStageBaseArea Supper;

public:
	USpaceStageCircleArea();
	~USpaceStageCircleArea();
	/**
	*初始化触发副本阶段目标完成的圆形区域数据
	*
	*@param StageIndex 副本阶段ID
	*@param TaskIndex 任务目标ID
	*@param CeilHeight 天空高度
	*@param FloorHeight 地面高度
	*@param AreaParam Range值和Point值
	*
	*@return 无
	*/
	void InitParams(FString ScriptID, INT32 StageIndex, INT32 TaskIndex, float CeilHeight, float FloorHeight, FString AreaParam) override;
	/**
	*判断参数位置是否在区域范围内
	*
	*@param Position 位置
	*
	*@return bool 参数位置在区域范围内返回true，否则为false
	*/
	bool IsPlayerIn() override;

protected:	
	FVector Point=FVector::ZeroVector;///<中心点
	float Range=0.0f;///<半径
};

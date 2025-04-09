// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/SpaceStageBaseArea.h"
#include "SpaceStagePolyArea.generated.h"

/**
* 文件名称：SpaceStagePolyArea.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-03-01
*/

/**
 * 触发副本阶段目标完成的多边形区域类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceStagePolyArea : public USpaceStageBaseArea
{
	GENERATED_BODY()
		typedef USpaceStageBaseArea Supper;
	
public:
	USpaceStagePolyArea();
	~USpaceStagePolyArea();
	/**
	*初始化触发副本阶段目标完成的多边形区域数据
	*
	*@param StageIndex 副本阶段ID
	*@param TaskIndex 任务目标ID
	*@param CeilHeight 天空高度
	*@param FloorHeight 地面高度
	*@param AreaParam Point坐标值
	*
	*@return 无
	*/
	void InitParams(FString ScriptID, INT32 StageIndex, INT32 TaskIndex, float CeilHeight, float FloorHeight, FString AreaParam) override;
	
};

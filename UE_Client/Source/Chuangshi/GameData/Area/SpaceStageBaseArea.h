// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/BaseArea.h"
#include "SpaceStageBaseArea.generated.h"

/**
* 文件名称：SpaceStageBaseArea.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-03-01
*/

/**
 * 触发副本阶段任务区域类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceStageBaseArea : public UBaseArea
{
	GENERATED_BODY()

public:
	USpaceStageBaseArea();
	~USpaceStageBaseArea();

	/**
	*初始化副本阶段任务区域数据
	*
	*@param StageIndex 副本阶段ID
	*@param TaskIndex 任务目标ID
	*@param CeilHeight 天空高度
	*@param FloorHeight 地面高度
	*@param AreaParam 区域参数3
	*
	*@return 无
	*/
	virtual void InitParams(FString ScriptID, INT32 StageIndex, INT32 TaskIndex, float CeilHeight, float FloorHeight, FString AreaParam);

	/**
	*进入SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	void OnEnter(const FString SpaceScriptID) override;
	
public:
	INT32 StageIndex; ///<副本阶段ID
	INT32 TaskIndex;///<任务目标ID
	INT32 AreaIndex;	///<用于标识是哪个区域
};

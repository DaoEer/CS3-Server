// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Quest/QuestBase/QuestTaskBase.h"
#include "QuestTaskGetTo.generated.h"

/**
* 文件名称：QuestTaskGetTo.h
* 功能说明：任务目标：到达某地
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UQuestTaskGetTo : public UQuestTaskBase
{
	GENERATED_BODY()
	
public:
	/**
	*初始化任务数据
	*
	*@param FQuestID 任务ID
	*@param FTaskID 任务目标ID
	*@param Param1 参数1
	*@param Param2 参数2
	*@param Param3 参数3
	*@param FProgress 任务目标进度
	*@param FGoal 任务目标数量
	*
	*@return 无
	*/
	virtual void InitDatas(const int32& FQuestID, const FCS3Task& _Task)override;
	
	
};

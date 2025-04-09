// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Quest/QuestBase/QuestBase.h"
#include "QuestLoop.generated.h"

/**
* 文件名称：QuestLoop.h
* 功能说明：环任务
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UQuestLoop : public UQuestBase
{
	GENERATED_BODY()

	typedef UQuestBase Supper;

public:
	/**
	*初始化任务数据
	*
	*@param FCS3QuestInfo 任务数据
	*
	*@return 无
	*/
	virtual void InitDatas(const FString JsonStr) override;

	
	/**
	*BlueprintCallable，获取任务环数
	*
	*
	*@return int32
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		int32 GetLoopQuestNum();

protected:
	int32 loopQuestNum;
	
	
	
};

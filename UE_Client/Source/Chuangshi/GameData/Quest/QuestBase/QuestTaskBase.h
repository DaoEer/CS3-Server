// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Quest/CS3QuestInfo.h"
#include "QuestTaskBase.generated.h"

/**
* 文件名称：QuestTaskBase.h
* 功能说明：任务目标基类
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UQuestTaskBase : public UCS3Object
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
	virtual void InitDatas(const int32& FQuestID, const FCS3Task& _Task);

	/*设置完成状态*/
	virtual void SetDone();
	/**
	*任务目标状态是否等于Status
	*
	*@param Status 任务状态
	*
	*@return bool 任务目标状态等于Status返回True，否则返回
	*/
	virtual bool IsTaskStatus(int32 Status);

	/**
	*更新任务进度
	*
	*@param Progress_ 任务进度
	*
	*@return 无
	*/
	void Update(const int32& Progress_);

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		int32 GetQuestID() { return QuestID; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		int32 GetTaskID() { return TaskID; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskName() { return TaskName; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		int32 GetProgress() { return Progress; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		int32 GetGoal() { return Goal; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		int32 GetPriority() { return Priority; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskClass() { return TaskClass; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskParam1() { return TaskParam1; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskParam2() { return TaskParam2; }

	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskParam3() { return TaskParam3; }
		
	UFUNCTION(BlueprintCallable, Category = "QuestTask")
		FString GetTaskNavigateData() { return NavigateData; }

protected:
	int32 QuestID;///<任务ID
	int32 TaskID;///<任务目标ID
	FString TaskName;///<任务目标名称
	int32 Progress;///<任务进度
	int32 Goal;///<任务数量
	int32 Priority;///<任务目标优先级
	FString TaskClass;///<任务目标Class
	FString TaskParam1;///<任务目标参数1
	FString TaskParam2;///<任务目标参数2
	FString TaskParam3;///<任务目标参数3
	FString NavigateData;///<任务目标寻路数据


};


/**
* 
* 功能说明：与传话任务NPC对话
*/
UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UQuestTaskTalkWithWhisper : public UQuestTaskBase
{
	GENERATED_BODY()

public:
	/*设置完成状态*/
	virtual void SetDone();
	/**
	*任务目标状态是否等于Status
	*
	*@param Status 任务状态
	*
	*@return bool 任务目标状态等于Status返回True，否则返回
	*/
	virtual bool IsTaskStatus(int32 Status);

protected:
	bool IsComplete = false;
};
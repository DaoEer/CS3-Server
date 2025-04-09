// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/Quest/QuestBase/QuestTaskBase.h"
#include "GameData/Quest/CS3QuestInfo.h"
#include "QuestBase.generated.h"

/**
* 文件名称：QuestBase.h
* 功能说明：任务基类
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FQuestInfoChangeDelegate, int32, QuestID, int32, TaskID, int32, Progress);

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UQuestBase : public UCS3Object
{
	GENERATED_BODY()
	
public:
	/**
	*初始化任务数据
	*
	*@param FCS3QuestInfo 任务数据
	*
	*@return 无
	*/
	virtual void InitDatas(const FString JsonStr);

	/**
	*BlueprintCallable，获取任务ID
	*
	*@return int32 任务ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		int32 GetID() { return ID; }

	/**
	*BlueprintCallable，获取下一个任务ID
	*
	*@return int32 下一个任务ID
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		int32 GetNextQuestID() { return nextQuestID; }

	/**
	*BlueprintCallable，获取任务名
	*
	*@return FString 任务名
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		FString GetQuestName() { return QuestName; }

	/**
	*BlueprintCallable，获取任务描述
	*
	*@return FString 任务描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		FString GetLogDesc() { return LogDesc; }

	/**
	*BlueprintCallable，获取任务NPC对话的描述
	*
	*@return FString 任务NPC对话的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		FString GetDescription() { return Description; }

	/**
	*BlueprintCallable，获取任务类型
	*
	*@return QUEST_TYPE 任务类型
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		QUEST_TYPE GetType() { return Type; }

	/**
	*BlueprintCallable，获取任务奖励
	*
	*@return TArray<FCS3RewardInfo> 任务奖励
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		TArray<FCS3RewardInfo> GetRewardInfo() { return RewardInfo; }

	/**
	*BlueprintCallable，获取任务状态
	*
	*@return QUEST_STATE 任务状态
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		QUEST_STATE GetState();

	/**
	*BlueprintCallable，获取是否自动接任务
	*
	*@return bool 自动接任务返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		bool IsAutoAccept() { return bIsAutoAccept; }

	/**
	*BlueprintCallable，获取是否自动交任务
	*
	*@return bool 自动交任务返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		bool IsAutoCommit() { return bIsAutoCommit; }

	/**
	*BlueprintCallable，获取任务目标
	*
	*@param TaskID 任务目标ID
	*
	*@return UQuestTaskBase* 任务目标
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		UQuestTaskBase* GetTask(const int32 TaskID);

	/**
	*BlueprintCallable，获取任务目标列表
	*
	*
	*@return UQuestTaskBase* 任务目标列表
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		TArray<UQuestTaskBase*> GetTasks();

	/**
	*更新任务目标数据
	*
	*@param TaskID 任务目标ID
	*@param Progress 任务目标进度
	*
	*@return 无
	*/
	void UpdateTask(const int32& TaskID, const int32& Progress);
	/**
	*设置任务目标完成
	*
	*@param TaskID 任务目标ID
	*
	*@return 无
	*/
	void SetTaskDone(const int32& TaskID);

	void SetTasksSortByPriority();

	bool IsPriorityTasksInViewTasks(const int32 Priority);

	/**
	*更新任务状态
	*
	*@param NewState 新任务状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		void SetState(const QUEST_STATE& NewState);

	/**
	*设置界面可见的任务目标列表ViewTasks
	*
	*@param  无
	*
	*@return 无
	*/
	void SetListViewTasksAndLastPriorityIndex();

	/**
	*同一优先级下的任务是否都完成
	*
	*@param  Priority 目标优先级
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		bool IsSamePriorityTasksHasDone(const int32 Priority );

	/**
	*是否为区分任务优先级的任务
	*
	*@param  无
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		bool IsPriorityTasksQuest();

	/**
	*指定优先级下是否有一个任务目标已完成
	*
	*@param Priority 目标优先级
	*
	*@return bool
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		bool IsHasAnyTaskDone(const int32 Priority);

	void Complete();///<任务完成

	UFUNCTION(BlueprintCallable, Category = "Quest")
		FString GetFinishBy() { return Finish_by; }

public:
	/**
	*任务目标改变事件委托
	*
	*@param QuestID 任务ID
	*@param TaskID 任务目标ID
	*@param Progress 任务目标进度
	*
	*@return 无
	*/
	UPROPERTY(BlueprintAssignable)
		FQuestInfoChangeDelegate OnQuestTaskChange;

protected:
	int32 ID;///<任务ID、下一个任务ID
	int32 nextQuestID;///<下一个任务ID
	FString QuestName;///<任务名
	FString LogDesc;///<任务描述
	FString Description;///<任务NPC对话的描述
	QUEST_TYPE Type;///<任务类型
	TArray<FCS3RewardInfo> RewardInfo;///<任务奖励
	QUEST_STATE State;///<任务状态
	bool bIsAutoAccept;///<是否自动接任务
	bool bIsAutoCommit;///<是否自动交任务
	FString Finish_by;///<交任务NPC的ScriptID

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "Quest")
	TMap<int32,UQuestTaskBase*> Tasks;///<任务目标

	TMap<int32, TArray<UQuestTaskBase*>> TaskMap;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "Quest")
		TArray<UQuestTaskBase*> ViewTasks;///<界面显示的任务目标

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "Quest")
		int32 LastTaskPriorityIndex;///<最后显示的任务目标优先级索引

};

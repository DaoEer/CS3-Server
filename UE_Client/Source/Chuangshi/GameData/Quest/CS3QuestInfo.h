// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CS3RewardInfo.h"
#include "CS3QuestInfo.generated.h"

/**
* 文件名称：CS3QuestInfo.h
* 功能说明：服务器传输到客户端的任务数据
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3Task
{
	GENERATED_USTRUCT_BODY()
public:
	//任务目标ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskID")
		int32 TaskID = 0;
	//任务目标实例
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskClass")
		FString TaskClass;
	//任务目标名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskName")
		FString TaskName;
	//任务目标记录
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Goal")
		int32 Goal = 0;
	//任务目标进度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Progress")
		int32 Progress = 0;
	//任务目标参数1
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskParam1")
		FString TaskParam1;
	//任务目标参数2
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskParam2")
		FString TaskParam2;
	//任务目标参数3
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskParam3")
		FString TaskParam3;
	//任务目标优先级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Priority")
		int32 Priority = 0;
	//寻路数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NavigateData")
		FString NavigateData;
};


USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3QuestInfo
{
	GENERATED_USTRUCT_BODY()
public:
	//任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ID")
		int32 ID = 0;
	//任务名
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "QuestName")
		FString QuestName;
	//任务类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Type")
		QUEST_TYPE Type;
	//任务描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Description")
		FString Description;
	//任务目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Task")
		TArray<FCS3Task> Tasks;
	//任务奖励
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardInfo")
		TArray<FCS3RewardInfo> RewardInfo;
	//任务状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "State")
		QUEST_STATE State;
	//任务描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "LogDesc")
		FString LogDesc;
	
	//是否自动接任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IsAutoAccept")
		bool IsAutoAccept;
	//是否自动交任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "IsAutoCommit")
		bool IsAutoCommit;
	//下一个任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NextQuestID")
		int32 NextQuestID = 0;
	// 环任务（环任务数量）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "loopQuestNum")
		int32 loopQuestNum = 0;
	// 交任务NPC的ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Finish_by")
		FString Finish_by;

};
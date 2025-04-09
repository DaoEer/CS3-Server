// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CS3RewardInfo.h"
#include "GameData/CsvTableRowBase.h"
#include "ClientQuestInfo.generated.h"
/**
* 文件名称：ClientQuestInfo.h
* 功能说明：客户端的任务数据
* 文件作者：Lintongbin
* 目前维护：Lintongbin
* 创建时间：2019-08-28
*/

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3QuestTask
{
	GENERATED_USTRUCT_BODY()
public:
	//任务目标ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ID")
		int32 ID = 0;
	//任务目标实例
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TaskClass")
		FString TaskClass;
	//任务目标名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Name")
		FString Name;
	//任务目标记录
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Goal")
		int32 Goal = 0;
	//任务目标参数1
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Param1")
		FString Param1;
	//任务目标参数2
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Param2")
		FString Param2;
	//任务目标参数3
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Param3")
		FString Param3;
	//任务目标优先级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Priority")
		int32 Priority = 0;
	//寻路数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NavigateData")
		FString NavigateData;
};

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3QuestRewards
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsScript")
		FString Script;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam1")
		FString Param1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam2")
		FString Param2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam3")
		FString Param3;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Description")
		FString Description;
};

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3QuestRequirements
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsScript")
		FString Script;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam1")
		FString Param1;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam2")
		FString Param2;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam3")
		FString Param3;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam4")
		FString Param4;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardsParam5")
		FString Param5;
};

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3ClientQuestInfo : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ID;
	//任务名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Title;
	//任务描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;
	//任务目标
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCS3QuestTask> Tasks;
	//未完成语音
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString unFinishTaskDes;
	//完成语音
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FinishTaskDes;
	//是否自动交接任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 isAutoQuest;
	//是否可共享
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32  CanShare;
	//任务类
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString  QuestClass;
	//任务脚本类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString  Script;
	//任务奖励
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCS3QuestRewards> Rewards;
	//可接取任务前提条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCS3QuestRequirements> Requirements;
	//是否自动接任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IsAutoAccept;
	//是否自动交任务
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IsAutoCommit;
	//从哪里开始
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Start_By;
	//等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level;
	//下一个任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString NextQuest;
	//是否可放弃
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CanAbandon;
	//任务过程描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TaskLogDes;
	//交任务NPC的ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Finish_by;
};
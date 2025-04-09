// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "PlaneTrigger.generated.h"

/**
* 文件名称：PlaneTrigger.h
* 功能说明：位面触发条件（用于判断进入位面的条件）
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-12
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPLANE_TRIGGER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	/// 代码不读取，便于策划查看
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlaneTrigger", DisplayName = "AreaName")
		FString AreaName;
	/// 进入位面的等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlaneTrigger", DisplayName = "Level")
		int32 Level = 0;
	/// 进入位面的阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlaneTrigger", DisplayName = "Camp")
		int32 Camp = 0;
	/// 任务条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlaneTrigger", DisplayName = "QuestCondition")
		FString QuestCondition;
	/// 是否是区域触发
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlaneTrigger", DisplayName = "isAreaTrigger")
		bool isAreaTrigger;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		const FString FirstSplitIns = FString(TEXT("|"));
		const FString SecondSplitIns = FString(TEXT(";"));
		const FString ThirdSplitIns = FString(TEXT(":"));

		TArray<FString> FSplitArray = SplitString(QuestCondition, true, FirstSplitIns);
		for (FString FSplitStr : FSplitArray)
		{

			TArray<FString> SSplitArray = SplitString(FSplitStr, true, SecondSplitIns);

			for (FString SSplitStr : SSplitArray)
			{
				FString QRightST, QLeftST;
				SSplitStr.Split(ThirdSplitIns, &QLeftST, &QRightST);
				if ((QRightST.TrimStartAndEnd() != "0" && FSTRING_TO_INT(QRightST) == 0)
					||(QLeftST.TrimStartAndEnd() != "0" && FSTRING_TO_INT(QLeftST) == 0))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"QuestCondition\" config error"));
					break;
				}
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/**
任务条件
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPlaneTriggerQuestCondition
{
	GENERATED_USTRUCT_BODY()

public:
	///任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QuestID = 0;

	///任务状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QuestState = 0;

	///任务目标状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, int32> TaskStates;
};

/**
解析后的位面触发条件
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FPlaneTriggerCondition
{
	GENERATED_USTRUCT_BODY()

public:
	///等级条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level = 0;

	///阵营条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	
	///任务条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FPlaneTriggerQuestCondition> QuestCondition;

	///是否是区域触发
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool isAreaTrigger;
};
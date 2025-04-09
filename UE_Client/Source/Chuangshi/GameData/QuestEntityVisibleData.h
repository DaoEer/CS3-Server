// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/GameDefine.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "QuestEntityVisibleData.generated.h"

/**
* 文件名称：QuestEntityVisibleData.h
* 功能说明：任务entity可见性配置相关结构体定义
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-4-27
*/

///任务状态
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQEV_SITUATION_STUCT
{
	GENERATED_USTRUCT_BODY()

public:
	/** 任务状态 */
	TArray<int32> QuestStates;

	/** 任务目标ID和状态 */
	TMap<int32,TArray<int32>> TaskStates;
};


///一个任务的可见状态和不可见状态
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQEV_ONE_QUEST_SITUATION
{
	GENERATED_USTRUCT_BODY()

public:
	/** 可见任务状态 */
	FQEV_SITUATION_STUCT* VisibleSituation;

	/** 不可见任务状态 */
	FQEV_SITUATION_STUCT* InvisibleSituation;

	/**任务目标优先级*/
	TArray<int32> TaskPriority;
};


///一个Entity的可见任务状态和不可见任务状态
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQEV_ONE_ENTITY_SITUATION
{
	GENERATED_USTRUCT_BODY()

public:
	/** 任务状态 */
	TMap<int32, FQEV_ONE_QUEST_SITUATION*> QuestSituations;

	/** 任务优先级 */
	TArray<int32> Priority;
};


///配置表行数据结构体
USTRUCT(BlueprintType)
struct CHUANGSHI_API FQEV_CFG_ROW_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	/** entity说明 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EntityNote;
	
	/** 地图说明 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpaceNote;

	/** 使Entity可见的任务状态 参数配置：任务ID1;任务状态1;任务状态2 例：20102000;3;4|20102002;4 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString VisibleQuestState;

	/** 可见任务目标状态 参数配置：任务ID;任务目标ID:任务目标状态 例：20102000;1:2;2:2|20102001;1:3 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString VisibleTaskState;

	/** 使Entity不可见的任务状态 参数配置：任务ID1;任务状态1;任务状态2 例：20102000;3;4|20102002;4 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString InvisibleQuestState;

	/** 不可见任务目标状态 参数配置：任务ID;任务目标ID:任务目标状态 例：20102000;1:2;2:2|20102001;1:3 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString InvisibleTaskState;

	/** 任务优先级 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Priority;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		bool EntityNoteResult = !EntityNote.IsEmpty();
		bool SpaceNoteResult = !SpaceNote.IsEmpty();
		if (!EntityNoteResult) ResultInfo.CheckLog += FString::Printf(TEXT("EntityNote cannot be empty!  "));
		if (!SpaceNoteResult) ResultInfo.CheckLog += FString::Printf(TEXT("SpaceNote cannot be empty!  "));
		bool VisibleQuestStateResult = true;
		if (!VisibleQuestState.IsEmpty())
		{
			for (auto datas : UGolbalBPFunctionLibrary::SplitString(VisibleQuestState, false, TEXT("|")))
			{
				for (auto data : UGolbalBPFunctionLibrary::SplitString(datas, false, TEXT(";")))
				{
					if (!data.TrimStartAndEnd().IsNumeric())
					{
						VisibleQuestStateResult = false;
						ResultInfo.CheckLog += FString::Printf(TEXT("VisibleQuestState: \"%s\" is config error!  "), *VisibleQuestState);
						break;
					}
				}
				if (VisibleQuestStateResult == false) break;
			}
		}
		bool VisibleTaskStateResult = true;
		if (!VisibleTaskState.IsEmpty())
		{
			for (auto datas : UGolbalBPFunctionLibrary::SplitString(VisibleTaskState, false, TEXT("|")))
			{
				int index = 0;
				for (auto data : UGolbalBPFunctionLibrary::SplitString(datas, false, TEXT(";")))
				{
					if (index == 0 && !data.TrimStartAndEnd().IsNumeric())
					{
						VisibleTaskStateResult = false;
						ResultInfo.CheckLog += FString::Printf(TEXT("VisibleTaskState: \"%s\" is config error!  "), *VisibleQuestState);
						break;
					}
					else
					{
						for (auto id : UGolbalBPFunctionLibrary::SplitString(data, false, TEXT(":")))
						{
							if (!id.TrimStartAndEnd().IsNumeric())
							{
								VisibleTaskStateResult = false;
								ResultInfo.CheckLog += FString::Printf(TEXT("VisibleTaskState: \"%s\" is config error!  "), *VisibleQuestState);
								break;
							}
						}
					}
					index++;
				}
				if (VisibleTaskStateResult == false) break;
			}
		}
		bool InvisibleQuestStateResult = true;
		if (!InvisibleQuestState.IsEmpty())
		{
			for (auto datas : UGolbalBPFunctionLibrary::SplitString(InvisibleQuestState, false, TEXT("|")))
			{
				for (auto data : UGolbalBPFunctionLibrary::SplitString(datas, false, TEXT(";")))
				{
					if (!data.TrimStartAndEnd().IsNumeric())
					{
						InvisibleQuestStateResult = false;
						ResultInfo.CheckLog += FString::Printf(TEXT("InvisibleQuestState: \"%s\" is config error!  "), *InvisibleQuestState);
						break;
					}
				}
				if (InvisibleQuestStateResult == false) break;
			}
		}
		bool InvisibleTaskStateResult = true;
		if (!InvisibleTaskState.IsEmpty())
		{
			for (auto datas : UGolbalBPFunctionLibrary::SplitString(InvisibleTaskState, false, TEXT("|")))
			{
				int index = 0;
				for (auto data : UGolbalBPFunctionLibrary::SplitString(datas, false, TEXT(";")))
				{
					if (index == 0 && !data.TrimStartAndEnd().IsNumeric())
					{
						InvisibleTaskStateResult = false;
						ResultInfo.CheckLog += FString::Printf(TEXT("InvisibleTaskState: \"%s\" is config error!  "), *InvisibleTaskState);
						break;
					}
					else
					{
						for (auto id : UGolbalBPFunctionLibrary::SplitString(data, false, TEXT(":")))
						{
							if (!id.TrimStartAndEnd().IsNumeric())
							{
								InvisibleTaskStateResult = false;
								ResultInfo.CheckLog += FString::Printf(TEXT("InvisibleTaskState: \"%s\" is config error!  "), *InvisibleTaskState);
								break;
							}
						}
					}
					index++;
				}
				if (InvisibleTaskStateResult == false) break;
			}
		}
		bool PriorityResult = true;
		if (!Priority.IsEmpty())
		{
			for (auto data : UGolbalBPFunctionLibrary::SplitString(Priority, false, TEXT("|")))
			{
				if (!data.TrimStartAndEnd().IsNumeric())
				{
					PriorityResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("Priority: \"%s\" is config error!  "), *Priority);
					break;
				}
			}
		}
		if (EntityNoteResult && SpaceNoteResult && VisibleQuestStateResult && VisibleTaskStateResult && InvisibleQuestStateResult && InvisibleTaskStateResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};
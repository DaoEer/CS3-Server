// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "LBCTaskDatas.generated.h"


/**
* 文件名称：LBCTaskDatas.h
* 功能说明：练兵场练兵任务数据 JIRA CST-11222 
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-7-8
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLBCTASKDATA :public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	/// 等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	/// 描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString tips = "";
	/// 经验奖励
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 rewardExp = 0;

};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Chinese.generated.h"
/**
* 文件名称：Chinese.h
* 功能说明：中文文字配置表
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-17
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FChinese : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Chinese")
		FString ChineseStr;

public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) {
		FString TempChineseSre = this->ChineseStr.TrimStartAndEnd();
		bool IsError = TempChineseSre.IsEmpty();
		if (IsError)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("Chinese Str Format Is Empty!\n"));
		}
		else {
			ResultInfo.Result = Ok;
		}
	}

	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};
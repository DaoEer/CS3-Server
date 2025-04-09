// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "BuffEntityVisibleData.generated.h"

/**
* 文件名称：BuffEntityVisibleData.h
* 功能说明：Buff entity可见性配置相关结构体定义
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-8-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBEV_CFG_ROW_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	/** entity说明 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EntityNote;

	/** 地图说明 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpaceNote;

	/** 使Entity可见的BuffID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 VisibleBuffID = 0;

	/** 使Entity不可见的BuffID */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 InvisibleBuffID = 0;

	/** Buff优先级 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Priority;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		if (Priority.IsEmpty())
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			for (auto data : UGolbalBPFunctionLibrary::SplitString(Priority))
			{
				if (!data.TrimStartAndEnd().IsNumeric())
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("Priority: \"%s\" is config error!\n"), *Priority);
					return;
				}
			}
			ResultInfo.Result = Ok;
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};

};
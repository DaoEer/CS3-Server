// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "CsvConfigData.generated.h"

/**
* 文件名称：CsvConfigData.h
* 功能说明：CSV配置数据
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCSV_CONFIG_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///配置提示信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "HintDesc")
	FString HintDesc;
	///配置加载路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "ConfigPath")
	TSoftObjectPtr<UDataTable> ConfigPath;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "PreLoad")
	bool PreLoading = true;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (HintDesc.TrimStartAndEnd().IsEmpty())
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("HintDesc cannot be empty!  "));
		}
		if (ConfigPath.ToSoftObjectPath().IsValid())
		{
			if (CheckIsScriptPackage(ConfigPath.ToString()))
			{
				if (!CheckScriptSoftPtrIsValid(ConfigPath))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("\"ConfigPath\" resource does not exist!\n"));
				}
			}
			else if(!CheckResourceFileIsExist(ConfigPath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("\"ConfigPath\" resource does not exist!\n"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("\"ConfigPath\" config is None!\n"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

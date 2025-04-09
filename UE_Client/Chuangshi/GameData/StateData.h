// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/GameDeFine.h"
#include "GameData/CsvTableRowBase.h"
#include "StateData.generated.h"

/**
 * 文件名称：StateData.h
 * 功能说明：人物状态数据表
 * 文件作者：JACK
 * 创建时间：2016/11/2 15:25
 * 更改记录:
 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTATE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "State")
	ENTITY_STATE State;
	///当前状态进入时对应的动作
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "ActionId")
	int32 ActionId = 0;
	///当前状态进入时对应的动作
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "CsvCongData", DisplayName = "StateClass")
	UClass* StateClass;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		bool StateResult = State >= (ENTITY_STATE)0 && State <= (ENTITY_STATE)9;
		if (!StateResult) ResultInfo.CheckLog += FString::Printf(TEXT("State is config error!  "));
		bool StateClassResult = true;
		if (IsValid(StateClass))
		{
			if (!CheckIsScriptPackage(StateClass->GetPathName()))
			{
				if (!CheckResourceFileIsExist(StateClass->GetPathName()))
				{
					StateClassResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("StateClass resource does not exist!  "));
				}
			}
		}
		else
		{
			StateClassResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("StateClass config is None!  "));
		}
		if (StateResult && StateClassResult)
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
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};

#pragma once
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "IntensifyCost.generated.h"

/**
* 文件名称：IntensifyCost.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-09-12
*/

/************************************************************************/
/* 装备强化消耗配置表*/
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FIntensifyCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MinMaxLv;
	///强化等级（级）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IntensifyLv = 0;
	///消耗白色晶石数量（个）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LowMaterialCost = 0;
	///消耗五彩晶石数量（个）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MediumMaterialCost = 0;
	///消耗超级晶石数量（个）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 HighMaterialCost = 0;
	///消耗金钱数量（铜）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MoneyCost = 0;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		FString Left;
		FString Right;
		MinMaxLv.Split(TEXT("-"), &Left, &Right);
		if (FSTRING_TO_INT(Left) == 0 || FSTRING_TO_INT(Right) == 0)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"MinMaxLv\" config error"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

/************************************************************************/
/* 装备强化备份、还原消耗配置表*/
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FIntensifyRestoreCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MinMaxLv;
	///备份装备强化，消耗金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SaveMoneyCost = 0;
	///备份装备强化，消耗北斗符
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SaveBeidouFuCost = 0;
	///还原装备强化，消耗金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RestoreMoneyCost = 0;
	///还原装备强化，消耗北斗符
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RestoreBeidouFuCost = 0;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		FString Left;
		FString Right;
		MinMaxLv.Split(TEXT("-"), &Left, &Right);
		if (FSTRING_TO_INT(Left) == 0 || FSTRING_TO_INT(Right) == 0)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"MinMaxLv\" config error"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
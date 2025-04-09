#pragma once
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "BackFireCost.generated.h"

/**
* 文件名称：BackFireCost.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-09-12
*/

/************************************************************************/
/* 装备回火消耗配置表                                                   */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBackFireCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(BlueprintReadOnly)
		FString MinMaxLv;
	///锁星数量
	UPROPERTY(BlueprintReadOnly)
		int32 BackFireLockCount = 0;
	///回火符
	UPROPERTY(BlueprintReadOnly)
		int32 LowMaterialCost = 0;
	///正阳符
	UPROPERTY(BlueprintReadOnly)
		int32 MediumMaterialCost = 0;
	///北斗符
	UPROPERTY(BlueprintReadOnly)
		int32 HighMaterialCost = 0;
	///消耗金钱数量（铜）
	UPROPERTY(BlueprintReadOnly)
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
/* 装备传星消耗配置表                                                   */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTransferIntensifyCost : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(BlueprintReadOnly)
		FString MinMaxLv;
	///锁星数量
	UPROPERTY(BlueprintReadOnly)
		int32 LockCount = 0;
	///回火符
	UPROPERTY(BlueprintReadOnly)
		int32 LowMaterialCost = 0;
	///正阳符
	UPROPERTY(BlueprintReadOnly)
		int32 MediumMaterialCost = 0;
	///北斗符
	UPROPERTY(BlueprintReadOnly)
		int32 HighMaterialCost = 0;
	///消耗金钱数量（铜）
	UPROPERTY(BlueprintReadOnly)
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
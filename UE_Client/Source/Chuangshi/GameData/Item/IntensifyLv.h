#pragma once
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "IntensifyLv.generated.h"

/**
* 文件名称：IntensifyLv.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-09-12
*/

/************************************************************************/
/* 装备强化次数和锁星数量配置表                                                                     */
/************************************************************************/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FIntensifyLv : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///<等级区间（级）
	///	如：“20-29”代表“等级大于等于20，并小于等于29”
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MinMaxLv;
	///<强化等级上限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxIntensifyLv = 0;
	///<锁星上限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxLockStar = 0;

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
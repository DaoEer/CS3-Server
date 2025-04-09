#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "MapConfigData.generated.h"

/**
* 文件名称：MapConfigData.h
* 功能说明：地图传送配置
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-06-21
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMapConfigData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///地图名，例 玉虚宫
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MapConfigData")
		FString MapName;
	///地图space名称，例 L_YXG
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MapConfigData")
		FString Space;
	///坐标位置，例 -25050 -314.521790
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MapConfigData")
		FString Position;
	///朝向，例 0 0 0
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MapConfigData")
		FString Direction = FString(TEXT("0 0 0"));

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		TArray<FString> PosData = SplitString(Position.TrimStartAndEnd(), false, " ");
		if (PosData.Num() == 3)
		{
			for (auto& Pos : PosData)
			{
				if (Pos.TrimStartAndEnd() != "0" && Pos.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Pos) == 0)
				{

					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Position\" config error"));
					break;
				}

			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Position\" config error"));
		}
		TArray<FString> DirData = SplitString(Direction.TrimStartAndEnd(), false, " ");
		if (DirData.Num() == 3)
		{
			for (auto& Dir : DirData)
			{
				if (Dir.TrimStartAndEnd() != "0" && Dir.TrimStartAndEnd() != "0.0" && FSTRING_TO_FLOAT(Dir) == 0)
				{

					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Direction\" config error"));
					break;
				}

			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Direction\" config error"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
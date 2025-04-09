#pragma once
#include "GameData/CsvTableRowBase.h"
#include "AuctionCfgData.generated.h"

/**
* 文件名称：AuctionCfgData.h
* 功能说明：掉落每轮竞拍的相关参数配置
* 文件作者：QRN
* 目前维护：QRN
* 创建时间：2020-08-26
*/

/**
*
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FAUCTIONCFG_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "name")
		FString name;
	///轮数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "index")
		int32 index;
	///每轮竞拍时长
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "time")
		int32 time;
	///每轮竞拍最低出价（百分比）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "price")
		int32 price;
};
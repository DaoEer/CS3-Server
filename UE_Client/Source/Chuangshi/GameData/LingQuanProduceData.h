// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "LingQuanProduceData.generated.h"

/**
* 文件名称：LingQuanProduceData.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-14
*/

///灵泉产出数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FLINGQUAN_PRODUCE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 产出的间隔时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LingQuanData", DisplayName = "TimeKey")
		int32 timeKey;
	//每隔多少时间产出的灵能数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LingQuanData", DisplayName = "OutLingNengAmount")
		int32  outLingNengAmount;
	//灵泉最大产出值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LingQuanData", DisplayName = "LingNengMaxAmount")
		int32  lingNengMaxAmount;
	//灵泉最大血量值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "LingQuanData", DisplayName = "LingQuanMaxHP")
		int32  lingQuanMaxHP;
};
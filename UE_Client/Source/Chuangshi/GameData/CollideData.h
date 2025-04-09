#pragma once

#include "CsvTableRowBase.h"
#include "CollideData.generated.h"

/**
* 文件名称：CollideData.h
* 功能说明：碰撞数据
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-13
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOLLIDE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///碰撞通道
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TEnumAsByte<ECollisionChannel> Channel;

	///忽略
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TEnumAsByte<ECollisionChannel>> IgnoreChannel;

	///重叠
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TEnumAsByte<ECollisionChannel>> OverlapChannel;
		
	///阻隔
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TEnumAsByte<ECollisionChannel>> BlockChannel;
};

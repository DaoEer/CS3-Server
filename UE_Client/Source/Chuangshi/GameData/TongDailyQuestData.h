#pragma once

#include "GameData/GameDefine.h"
#include "CsvTableRowBase.h"
#include "TongDailyQuestDATA.generated.h"

/**
* 文件名称：TongDailyQuestData.h
* 功能说明：帮会日常任务数据
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-4-20
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongDailyQuestTreeDATA
{
	GENERATED_BODY()
	///任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 questID = 0;
	// 任务树索引
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 nodeIndex = 0;
	///任务标题
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString title;
	///任务类别（0：休闲类，1：问答类，2：挑战类）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "genre")
		int32 genre = 0;
	/// 任务树层数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 layer = 0;
	///连接下一层的任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> route;
};

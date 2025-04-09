#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "WhisperQuestConfig.generated.h"

/**
* 文件名称：WhisperQuestConfig.h
* 功能说明：传话任务数据表
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-01-20
*/

//传话任务数据表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FWHISPER_QUEST_CONFIG : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///根任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		int32 rootQuestID;
	///任务目标编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		int32 taskID;
	///任务目标标题
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString taskName = "";
	///npcID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		int32 npcID = 0;
	///寻路数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString navigateData = "";
	///NPC开始对话ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString npcSoundID = "";
	///玩家开始对话ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString startSoundID = "";
	///传话成功对话ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString succeedSoundID = "";
	///传话失败对话ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString failedSoundID = "";
	///传话内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		FString dialogue = "";
	///子任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		int32 taskQuestID = 0;
	///子任务时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "WhisperQuestConfig")
		float taskQuestTime = 0;
};
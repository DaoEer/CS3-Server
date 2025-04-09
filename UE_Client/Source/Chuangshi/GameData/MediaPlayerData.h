// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CsvTableRowBase.h"
#include "../MediaAssets/Public/MediaSource.h"
#include "GameData/GameDeFine.h"
#include "MediaPlayerData.generated.h"

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKIP_Info
{
	GENERATED_USTRUCT_BODY()

	///几秒后可跳过（秒，＜0代表“不可以跳过”）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Skip;
	///是否显示SkipUI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsShowSkipUI = true;
};

/**
*	#Media数据
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FMEDIA_PLAYER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///视频资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<TSoftObjectPtr<UMediaSource>> MediaSources;
	///游戏状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<EGameStatus> GameStatus;
	///地图spaceID（如”L_YXG“，@DT_HashMapCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Space;
	///任务ID（@DT_QuestInfoCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestID;
	/*///是否屏蔽UI
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool HideUI;*/
	///是否循环
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Loop = false;
	///视频最短时间 -1表示不对视频时长限制 Loop=true时使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float MinimumTime = -1.0f;
	///播放速率（倍）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float Rate = 1.0f;
	///跳过相关
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FSKIP_Info SkipData;
	/** 是否进入世界时停止播放*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsStopInWorldOver = false;

	/** 是否过图停止播放镜头*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsStopLoadingLevel = true;

	/** 视频播放事件*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString OnMediaOpenedEvent;

	/** 视频停止事件*/
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString OnMediaStopedEvent ;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		for (int i = 0; i < MediaSources.Num(); i++)
		{
			auto& MediaData = MediaSources[i];
			if (MediaData.ToSoftObjectPath().IsValid())
			{
				if (!CheckResourceFileIsExist(MediaData.ToString()))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"MediaSources\" index(%d) resource does not exist"), i);
				}
			}
			else
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"MediaSources\" index(%d) config is None"), i);
			}
		}

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

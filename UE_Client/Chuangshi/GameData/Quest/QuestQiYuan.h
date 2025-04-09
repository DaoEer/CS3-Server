// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Quest/QuestBase/QuestBase.h"
#include "QuestQiYuan.generated.h"

/**
* 文件名称：QuestQiYuan.h
* 功能说明：奇缘任务
* 文件作者：qrn
* 目前维护：qrn
* 创建时间：2020-06-18
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UQuestQiYuan : public UQuestBase
{
	GENERATED_BODY()

public:
	/**
	*初始化任务数据
	*
	*@param FCS3QuestInfo 任务数据
	*
	*@return 无
	*/
	virtual void InitDatas(const FString JsonStr);

	/*
	*获取倒计时长
	*/
	UFUNCTION(BlueprintCallable, Category = "Quest")
		FString getCountDown() { return mCountDown; }

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "QuestQiYuan")
		int32 isShowTime; //1:需要显示倒计时   0：不需要显示倒计时

private:
	FString mCountDown;
};

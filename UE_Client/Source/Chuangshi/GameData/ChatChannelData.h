// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatType.h"
#include "ChatChannelData.generated.h"

/**
* 文件名称：ChatChannelData.h
* 功能说明：
* 文件作者：ouyangminzheng
* 目前维护：hejingke
* 创建时间：2016-11-17
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatChannelData
{
	GENERATED_USTRUCT_BODY()
		FChatChannelData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "channelType")
		ChatType channelType = ChatType::Nearby;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "isCanModify")
		int32 isCanModify = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "shortcutKey")
		FString shortcutKey;

};
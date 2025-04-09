// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/ChatPageType.h"
#include "GameData/ChatType.h"
#include "ChatPageData.generated.h"

/**
* 文件名称：ChatPageData.h
* 功能说明：
* 文件作者：ouyangminzheng
* 目前维护：hejingke
* 创建时间：2016-11-17
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FChatPageData
{
	GENERATED_USTRUCT_BODY()
		FChatPageData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "pageType")
		ChatPageType pageType = ChatPageType::Synthesis;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "isDeletable")
		int32 isDeletable = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "isDraggable")
		int32 isDraggable = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "pageName")
		FString pageName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "channelList")
		TArray<ChatType> channelList;
};
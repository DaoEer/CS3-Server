// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "MemoirData.generated.h"

/**
* 文件名称：MemoirData.h
* 功能说明：仙魔录数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-03-27
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMEMOIR_DATA : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "id")
	FString id;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "musicID")
	FString musicID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "movieID")
	FString movieID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "title")
	FString title;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "topic")
	FString topic;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "content")
	FString content;
};

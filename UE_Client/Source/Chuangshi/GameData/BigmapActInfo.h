// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatType.h"
#include "BigmapActInfo.generated.h"

/**
* 文件名称：BigmapActInfo.h
* 功能说明：活动中 大地图显示数据
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-10-24
*/


USTRUCT(BlueprintType)
struct CHUANGSHI_API FBigmapActInfo
{
	GENERATED_USTRUCT_BODY()
		FBigmapActInfo() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "objectID")
		int32 objectID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerName")
		FString playerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "position")
		FVector position = FVector::ZeroVector;

};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/GameDeFine.h"
#include "CS3RewardInfo.generated.h"

/**
* 文件名称：CS3RewardInfo.h
* 功能说明：任务奖励数据
* 文件作者：Chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-02-16
*/

USTRUCT(BlueprintType, Blueprintable)
struct CHUANGSHI_API FCS3RewardInfo
{
	GENERATED_USTRUCT_BODY()
public:
	//奖励类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardInfo")
		REWARED_TYPE Type;
	//数值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RewardInfo")
		FString Value;
};
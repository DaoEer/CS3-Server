// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SpaceStrategyPointData.generated.h"


/**
* 文件名称：SpaceStrategyPointData.h
* 功能说明：副本策略点
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-4-19
*/
USTRUCT(BlueprintType)
struct FSPACESTRATEGYPOINTDATA {
	GENERATED_USTRUCT_BODY()
	/// 策略点index
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Index = 0;
	/// 策略点描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Describe;
	/// 策略点相关值 ("*":策略点值，"?":策略点上限值，"(1)":条件1值，"(2)":条件2值)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<FString,int32> ValueMap;
	/// 策略点是否结束
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsEnd;
	/// 完成策略点奖励值 ("1":奖励经验值，"2":奖励的潜能值，"3":奖励的帮贡值)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32,int32> RewardMap;
	/// 策略点是否完成
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsSuccess;
	/// 策略点是否时间类型 (目的为了做客户端自己做个正计时 00:00)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsTimeType;
};
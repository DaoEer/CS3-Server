// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SpaceYXLMData.generated.h"


/**
* 文件名称：SpaceYXLMData.h
* 功能说明：英雄王座 JIRA CST-4260
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-6-27
*/

USTRUCT(BlueprintType)
struct FSPACEYXLMDATA {
	GENERATED_USTRUCT_BODY()
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	/// 玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayerName;
	/// 被击杀的次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BeKill = 0;
	/// 击杀其他玩家的次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Kill = 0;
	/// 玩家物品的ID列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> ItemIDList;
};
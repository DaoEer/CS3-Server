// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "YXLMMatchData.generated.h"


/**
* 文件名称：YXLMMatchData.h
* 功能说明：英雄王座 JIRA CST-4260
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-7-3
*/

USTRUCT(BlueprintType)
struct FYXLMMATCHDATA {
	GENERATED_USTRUCT_BODY()
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	/// 玩家ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Id = 0;
	/// 玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level = 0;
	/// 玩家名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
};
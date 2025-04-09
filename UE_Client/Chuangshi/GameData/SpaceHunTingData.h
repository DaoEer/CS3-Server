// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SpaceHunTingData.generated.h"


/**
* 文件名称：SpaceHunTingData.h
* 功能说明：晶石狩猎场 JIRA CST-2043
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-1-19
*/

USTRUCT(BlueprintType)
struct FSPACEHUNTING {
	GENERATED_USTRUCT_BODY()
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	/// 玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayerName;
	/// 职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Profession = 0;
	/// 等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level = 0;
	/// 金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Money = 0;
	/// 被击杀的次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BeKill = 0;
	/// 击杀其他玩家的次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Kill = 0;
};
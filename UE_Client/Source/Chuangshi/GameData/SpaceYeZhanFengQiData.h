// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SpaceYeZhanFengQiData.generated.h"

/**
* 文件名称：SpaceYeZhanFengQiData.h
* 功能说明：血斗凤栖镇 JIRA CST-3838
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-3-22
*/

USTRUCT(BlueprintType)
struct FSPACEYEZHANFENGQI {
	GENERATED_USTRUCT_BODY()
	/// 玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayerName;
	/// 职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Profession = 0;
	/// 击杀的其他玩家次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 KillNum = 0;
	/// 积分
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Integral = 0;
};
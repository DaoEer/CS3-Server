// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SGMZMatchData.generated.h"


/**
* 文件名称：SGMZMatchData.h
* 功能说明：上古密阵
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-11-18
*/

USTRUCT(BlueprintType)
struct FSGMZMATCHDATA {
	GENERATED_USTRUCT_BODY()
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 Camp = 0;
	/// 玩家ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 Id = 0;
	/// 玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 Level = 0;
	/// 玩家名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString Name;
	/// 职业
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 Profession = 0;
};

USTRUCT(BlueprintType)
struct FSGMZBOSSDATA {
	GENERATED_USTRUCT_BODY()
	/// Boss名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString bossName;
	/// 所获得经验
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 exp = 0;
	/// 评分等级 0：超凡 1：问鼎 2：出尘 3：入道
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 level = 0;
	/// 击杀所用时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 time = 0;
	/// 血量百分比
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		float PerHP = 0.0;
	///阶段
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 stage;
};

USTRUCT(BlueprintType)
struct FSGMZTEAM0DATA {
	GENERATED_USTRUCT_BODY()
	/// 队伍阵营
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 teamCamp = 0;
	/// 是否为胜利队伍
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 isWin = 0;
	/// 是否为击杀Boss的队伍
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 isKillBoss = 0;
	/// 额外经验
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 extraExp = 0;
	/// 比分
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 score = 0;
	/// 功勋
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 feats = 0;
	/// 击杀终极Boss的玩家Name
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString BossKiller;
	/// 各个Boss数据：FSGMZBOSSDATA
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FSGMZBOSSDATA> bossDatas;
};




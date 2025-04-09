// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "TongStarcraftData.generated.h"

/**
* 文件名称：TongStarcraftData.h
* 功能说明：帮会争霸 JIRA CST-4450
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-8-15
*/

USTRUCT(BlueprintType)
struct FFIRST_TONGSTARCRAFT_SIGNDATA {
	GENERATED_USTRUCT_BODY()
	/// 帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName;
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongLevel = 0;
};
USTRUCT(BlueprintType)
struct FFIRST_TONGSTARCRAFT_PASSDATA {
	GENERATED_USTRUCT_BODY()
	/// 帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName;
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongLevel = 0;
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PassTime = 0;
};
USTRUCT(BlueprintType)
struct FTHIRD_TONGSTARCRAFT_MEMBERDATA
{
	GENERATED_USTRUCT_BODY()
	/// 玩家名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString RoleName;
	/// 归属方0：红方 1：蓝方
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 TongSide = 0;
	/// 玩家ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 RoleID = 0;
	/// 玩家击杀数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Kill = 0;
	/// 玩家被击杀数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 BeKill = 0;
	/// 玩家助攻次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Assists = 0;
	/// 玩家占领水晶次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Occupy = 0;
};

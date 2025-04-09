// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "RoleArmyData.generated.h"



/**
* 文件名称：RoleArmyData.h
* 功能说明：玩家部队数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-26
*/

USTRUCT(BlueprintType)
struct FROLEARMYDATA {
	GENERATED_USTRUCT_BODY()
	/// id
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Id = 0;
	/// 部队是否忙碌（正在做任务）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BeBusy = 0;
	/// 亲卫的scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FirstGuardScriptID;
	/// 亲卫的scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SecondGuardScriptID;
	/// 兵的scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SoldierScriptID;
	/// 兵的IDs
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> SoldierIDs;
};


/// 练兵任务
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRAIN_GROUND_QUEST
{
	GENERATED_BODY()

public:
	/// 任务ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "QuestID")
		int32 QuestID = 0;
	/// 任务 标题
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Title")
		FString Title;
	/// 任务 目标描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TaskTitle")
		FString TaskTitle;
	/// 任务 奖励
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Reward")
		int32 Reward;
	/// 小兵scriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SoldierScriptID")
		FString SoldierScriptID;
	

};
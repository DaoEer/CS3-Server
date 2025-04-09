// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CombatDelegateObject.h"
#include "QuestDelegateObject.generated.h"

/**
 * 任务/对话 委托相关声明对象
 */

DECLARE_DYNAMIC_MULTICAST_DELEGATE_SevenParams(FOnShowTongDailyQuestSpaceWin, FString, Msg, FString, Statistics, FString, RewardStr, int32, GradeScore, int32, CountDown, FString, itemStr, FString, buff);
UCLASS()
class CHUANGSHI_API UQuestDelegateObject : public UCombatDelegateObject
{
	GENERATED_BODY()
public:

#pragma region	/** 帮会日常任务副本通关结算 */
	//打开淬炼界面
	UPROPERTY(BlueprintAssignable, Category = "SpaceContent|TongDailyQuest")
		FOnShowTongDailyQuestSpaceWin OnShowTongDailyQuestSpaceWin;
#pragma endregion
};

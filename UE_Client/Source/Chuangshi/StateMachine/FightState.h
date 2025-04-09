// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "BaseState.h"
#include "FightState.generated.h"

/*
* 文件名称：FightState.h
* 功能说明：人物战斗状态
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-11-01
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UFightState : public UBaseState
{
	GENERATED_BODY()
public:
	virtual void Enter() override;///< 刚进入时调用
	virtual void Execute() override;///< 执行时调用
	virtual void Exit() override;///< 离开时调用
};

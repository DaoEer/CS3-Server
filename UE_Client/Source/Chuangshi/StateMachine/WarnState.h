// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "StateMachine/BaseState.h"
#include "WarnState.generated.h"

/*
* 文件名称：RoleState.h
* 功能说明：玩家警戒状态
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-11-17
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UWarnState : public UBaseState
{
	GENERATED_BODY()
	
public:
	virtual void Enter() override;///< 刚进入时调用
	virtual void Execute() override;///< 执行时调用
	virtual void Exit() override;///< 离开时调用
	
	
};

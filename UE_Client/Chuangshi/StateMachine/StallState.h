// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "StateMachine/BaseState.h"
#include "StallState.generated.h"

/*
* 文件名称：StallState.h
* 功能说明：人物摆摊状态
* 文件作者：yikun
* 目前维护：chendongyong
* 创建时间：2017-04-13
*/


UCLASS(BlueprintType)
class CHUANGSHI_API UStallState : public UBaseState
{
	GENERATED_BODY()

public:
	virtual void Enter() override;///< 刚进入时调用
	virtual void Execute() override;///< 执行时调用
	virtual void Exit() override;///< 离开时调用


};

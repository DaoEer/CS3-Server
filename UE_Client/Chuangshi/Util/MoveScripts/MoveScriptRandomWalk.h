// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "MoveScriptBase.h"


/*
* 文件名称：MoveScriptRandomWalk.h
* 功能说明：客户端怪物控制移动类 随机移动
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-9
*/

class MoveScriptRandomWalk : public MoveScriptBase {
	typedef MoveScriptBase Super;
public:
	MoveScriptRandomWalk(APawn* InPawn, FVector _OriginalPos, float _RandomRange, float _AcceptanceRadius);
	virtual void DoMove() override;
	virtual void OnMoveOver() override;
	virtual void MoveReachCheck() override;
	FVector GetGoalPos();

private:
	FVector OriginalPos;
	FVector GoalPos;
	float RandomRange;
	
};
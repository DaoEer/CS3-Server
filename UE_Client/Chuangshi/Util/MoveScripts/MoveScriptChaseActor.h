// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "MoveScriptBase.h"
#include "GameFramework/Actor.h"


/*
* 文件名称：MoveScriptChaseActor.h
* 功能说明：客户端怪物控制移动类 追击Actor
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-9
*/

class MoveScriptChaseActor : public MoveScriptBase {
	typedef MoveScriptBase Super;

public:
	MoveScriptChaseActor(APawn* InPawn, AActor* _GoalActor, float _AcceptianRadius);
	virtual void DoMove() override;
	virtual void OnMoveOver() override;
	virtual void MoveReachCheck() override;
	AActor* GetGoalActor();
	FVector GetGoalPos();

private:
	AActor* GoalActor;
};
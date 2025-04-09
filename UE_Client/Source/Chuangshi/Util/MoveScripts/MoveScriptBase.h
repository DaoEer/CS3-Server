// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/Pawn.h"

/*
* 文件名称：MoveScriptBase.h
* 功能说明：客户端怪物控制移动类 基类
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-9
*/


class MoveScriptBase {
public:
	MoveScriptBase(APawn* InPawn, float _AcceptanceRaius);
	virtual ~MoveScriptBase() {};
	virtual void DoMove();
	virtual void MoveReachCheck();
	virtual void OnMoveOver();

	APawn* GetOwner();
	bool IsMoveOver();

protected:
	float AcceptanceRadius = 50.0;
	float MoveSpeed;
	bool bIsMoveOver = false;
private:
	APawn* Owner;
};


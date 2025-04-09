// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "FilterActorComponent.h"
#include "LineToPointFilterActorComponent.generated.h"

/*
* 文件名称：LineToPointFilterActorComponent.h
* 功能说明：客户端代替服务器做直线移动（服务器在高速移动时会卡顿）
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-1-10
*/

/**
 * 用于客户端模拟服务器做直线移动，服务器只负责设置最终位置
 */
UCLASS(BlueprintType)
class CHUANGSHI_API ULineToPointFilterActorComponent : public UFilterActorComponent
{	
	GENERATED_BODY()
	typedef UFilterActorComponent Supper;
public:
	virtual void SimulateMovement(float DeltaTime) override;
	void InitData(float InVelocity, const FVector& InDestPos);

public:
	float Velocity;         //移动速度
	FVector DestPos;		//目标位置
};

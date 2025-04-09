// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/EffectEmitter.h"
#include "DelegateCombinations.h"
#include "CircleEffectEmitter.generated.h"

/*
* 文件名称：CircleEffectEmitter.h
* 功能说明：做环形火焰蔓延的效果，类似的环形粒子缩放都可以用这个
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2020-5-21
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FCircleEffectOnStopMove);

UCLASS()
class CHUANGSHI_API ACircleEffectEmitter : public AEffectEmitter
{
	GENERATED_BODY()

public:
	ACircleEffectEmitter();
	
	//virtual void Tick(float DeltaSeconds) override;
	///初始化配置
	virtual void InitFromConfig();
	void SetCircleEffectParameter(bool InIsMove, float InStartSpawnNum, float InStartRadius, float InTotalTime, float InIntervalTime);
private:
	void Move();
	void StopMove();
public:
	///光效停止运动通知
	UPROPERTY(BlueprintAssignable)
		FCircleEffectOnStopMove OnCircleEffectStopMove;
private:
	float StartSpawnNum;
	float StartRadius;
	float TotalTime;
	float IntervalTime;
	float Radius;
	FTimerHandle timerHandle;
};

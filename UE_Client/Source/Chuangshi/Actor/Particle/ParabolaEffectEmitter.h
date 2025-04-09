// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/FlyEffectEmitter.h"
#include "ParabolaEffectEmitter.generated.h"

/*
* 文件名称：ParabolaEffectEmitter.h
* 功能说明：抛物线，根据Z轴的速度，从起点模拟抛物线到 终点
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2019-12-24
*/

UCLASS(abstract)
class CHUANGSHI_API AParabolaEffectEmitter : public AFlyEffectEmitter
{
	GENERATED_BODY()

public:
	virtual void Tick(float DeltaTime) override;

protected:

	///初始化位置
	virtual void InitEmitterTransform() override;


protected:
	FVector _FlySpeed;
	float GravityZ;

	
};

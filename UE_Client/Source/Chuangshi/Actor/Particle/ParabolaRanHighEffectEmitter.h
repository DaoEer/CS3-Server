// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/ParabolaEffectEmitter.h"
#include "ParabolaRanHighEffectEmitter.generated.h"

/*
* 文件名称：ParabolaRanHighEffectEmitter.h
* 功能说明：随机抛物线最高点，从始点到终点模拟抛物线
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-1-15
*/

UCLASS(abstract)
class CHUANGSHI_API AParabolaRanHighEffectEmitter : public AParabolaEffectEmitter
{
	GENERATED_BODY()
	

protected:

	///初始化位置
	virtual void InitEmitterTransform() override;
};

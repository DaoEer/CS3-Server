// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/EffectEmitter.h"
#include "TrailEffectEmitter.generated.h"
/*
* 文件名称：TrailEffectEmitter.h
* 功能说明：
* 文件作者：shengbing
* 目前维护：zhangfudong
* 创建时间：2017-07-15
*/
/**
 * 拖尾光效基类
 */
UCLASS(abstract)
class CHUANGSHI_API ATrailEffectEmitter : public AEffectEmitter
{
	GENERATED_BODY()
public:
	///重写，销毁拖尾粒子组件
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

protected:
	///重写，创建拖尾粒子组件
	virtual void StartPlay() override;

	///重写，暂停拖尾粒子组件
	virtual void DelayDestroySetting() override;

public:
	///拖尾模式
	UPROPERTY(BlueprintReadOnly)
	TEnumAsByte<enum ETrailWidthMode> WidthScaleMode;

private:
	///拖尾粒子组件
	UPROPERTY()
	UParticleSystemComponent* PSComponent;
};

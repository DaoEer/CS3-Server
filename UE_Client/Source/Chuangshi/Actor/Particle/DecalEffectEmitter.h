// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Actor/Particle/EffectEmitter.h"
#include "DecalEffectEmitter.generated.h"

/*
* 文件名称：DecalEffectEmitter.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：zhangfudong
* 创建时间：2017-07-19
*/

DECLARE_STATS_GROUP(TEXT("ADecalEffectEmitter"), STATGROUP_ADecalEffectEmitter, STATCAT_Advanced);

class ADecalEffect;

UCLASS(BlueprintType)
class CHUANGSHI_API ADecalEffectEmitter : public AEffectEmitter
{
	GENERATED_BODY()
public:
	///重写，销毁贴花
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	
	TArray<ADecalEffect*> GetDecalArr();
protected:
	///重写，播放贴花
	virtual void StartPlay() override;
	
	///重写，停止贴花
	virtual void DelayDestroySetting() override;

	///光效在生命周期淡入淡出
	virtual void UpdateTransparency(float DeltaSeconds) override;

	///重写，贴花不需要加
	virtual void AddAlphaModule(UParticleSystemComponent* ParticleComponent = nullptr) {}

protected:
	///贴花的实例
	UPROPERTY()
	TArray<ADecalEffect*> DecalArr;
};

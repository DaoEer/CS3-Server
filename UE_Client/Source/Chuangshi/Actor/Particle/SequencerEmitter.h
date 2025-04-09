// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Particles/Emitter.h"
#include "SequencerEmitter.generated.h"

/*
* 文件名称：SequencerEmitter.h
* 功能说明：
* 文件作者：jiangyupeng
* 目前维护：zhangfudong
* 创建时间：2017-10-27
*/
UCLASS(BlueprintType)
class CHUANGSHI_API ASequencerEmitter : public AEmitter
{
	GENERATED_BODY()
	
public:	
	
	UFUNCTION(BlueprintCallable, Category = "CustomParticle")
	void SetWarmupTime(float Value);

protected:
	// 经过的时间
	float DeltaTime;
	
};

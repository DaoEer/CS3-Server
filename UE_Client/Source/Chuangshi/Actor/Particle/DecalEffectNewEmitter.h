// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Particle/EffectEmitter.h"
#include "DecalEffectNewEmitter.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API ADecalEffectNewEmitter : public AEffectEmitter
{
	GENERATED_BODY()
	
public:
	///重写，销毁（新）贴花组件
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

protected:
	///重写，创建（新）贴花组件
	virtual void StartPlay() override;

};

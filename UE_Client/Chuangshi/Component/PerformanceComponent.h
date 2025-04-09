// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PerformanceComponent.generated.h"

/*
* 文件名称：PerformanceComponent.h
* 功能说明：用于统一处理对象特效的生命周期
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-08-27
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UPerformanceComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UPerformanceComponent();

	// 结束组件的时候销毁所有存储的粒子
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

	// 添加UID到列表
	FORCEINLINE void AddEffect(int32 EffectUID)
	{
		EffectUIDList.Add(EffectUID);
	}

private:	

	// 存储粒子的UID，只加入，不移除
	TArray<int32> EffectUIDList;
	
};

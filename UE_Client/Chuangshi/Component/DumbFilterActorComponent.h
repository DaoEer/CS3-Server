// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "FilterActorComponent.h"
#include "DumbFilterActorComponent.generated.h"

/*
* 文件名称：DumbFilterActorComponent.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

/**
 * 一个直接改变对象位置的过滤器，可用于传送等非移动引起的位置位置改变
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UDumbFilterActorComponent : public UFilterActorComponent
{	
	GENERATED_BODY()
	typedef UFilterActorComponent Supper;

public:
	virtual void SimulateMovement(float DeltaTime) override;
	virtual void OnUpdateVolatileData(const FVector& position, const FVector& direction, int32 parentID) override;
	virtual void SetPosition(const FVector& position, int32 parentID) override;
	virtual void SetDirection(const FVector& direction, int32 parentID) override;
	virtual void OnUpdateVolatileDataByParent(const FVector& position, const FVector& direction, int32 parentID) override;
};
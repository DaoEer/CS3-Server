// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "CS3Object.h"
#include "TickObject.generated.h"

/**
* 文件名称：TickObject.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UTickObject : public UCS3Object, public FTickableGameObject
{
	GENERATED_BODY()
public:
	UTickObject();
	virtual void PostInitProperties() override;
	virtual void BeginDestroy() override;
	~UTickObject();
	//tick时间间隔
	UPROPERTY(EditAnywhere, Category = "Tick")
		bool bCanEverTick = false;
	UPROPERTY(EditAnywhere, Category = "Tick", meta = (EditCondition = "bCanEverTick"))
		float CustomTimeDilation;
	
	virtual void TickObject() {}

	virtual void Tick(float DeltaTime);
	virtual bool IsTickable() const { return bCanEverTick; }
	virtual bool IsTickableInEditor() const { return (!GWorld->HasBegunPlay() && GIsEditor) ? false : true; }
	virtual bool IsTickableWhenPaused() const { return false; };
	FORCEINLINE TStatId GetStatId() const {	RETURN_QUICK_DECLARE_CYCLE_STAT(UTickObject, STATGROUP_Tickables);	}
	//表示处理PIE播放中或独立窗口
	bool IsPlaying();
	//表示处理游戏的InWorld中
	bool IsInWorld();
	//获取tick的总时间
	float GetSumTickTime() { return SumTickTime; }
private:
	float SumDeltaTime;
	float SumTickTime;	//记录已经tick的时间
	
};

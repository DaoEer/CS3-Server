// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseTask.h"
#include "MemoryTask.generated.h"

/*
* 文件名称：MemoryTask.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMEMRECORD
{
	GENERATED_USTRUCT_BODY()

public:
	FDateTime Time;
	float UsePhysical;	//使用了多少M内存
};

/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UMemoryTask : public UBaseTask
{
	GENERATED_BODY()
	
public:
	UMemoryTask();
	virtual void InitParam() override;	//解析参数一到参数五
	virtual void TickObject() override;		//tick task
	virtual bool Condition() override;

	//获取此地图上平均使用内存
	int32 GetAvgUseMemory();
	int32 GetMinUseMemory();
	int32 GetMaxUseMemory();

public:
	float LifeTime;		//需要记录的时间
	UPROPERTY(BlueprintReadWrite, Category = "Object")
		TArray<FMEMRECORD> MemRecords;
	
	
};

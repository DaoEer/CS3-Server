// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseTask.h"
#include "FrameTask.generated.h"

/*
* 文件名称：FrameTask.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/


USTRUCT(BlueprintType)
struct CHUANGSHI_API FFRAMERECORD
{
	GENERATED_USTRUCT_BODY()

public:
	FDateTime Time;
	float FPS;	//FPS
};

/**
 * 记录客户端的FPS
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UFrameTask : public UBaseTask
{
	GENERATED_BODY()
public:
	UFrameTask();
	virtual void InitParam() override;	//解析参数一到参数五
	virtual void TickObject() override;		//tick task
	virtual bool Condition() override;

	//获取此地图上平均帧率
	int32 GetAvgFrame();
	int32 GetMinFrame();
	int32 GetMaxFrame();

public:
	float LifeTime;		//需要记录的时间
	UPROPERTY(BlueprintReadWrite, Category = "Object")
		TArray<FFRAMERECORD> FrameRecords;
	
	
	
};

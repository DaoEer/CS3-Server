// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseTask.h"
#include "AutoTest/AutoTestDebug.h"
#include "ObjectTask.generated.h"

/*
* 文件名称：ObjectTask.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FOBJRECORD
{
	GENERATED_USTRUCT_BODY()

public:
	FDateTime Time;
	int32 ObjCounts;	//包括不会被GC的CDO对象
	int32 GCObjCounts;	//会被GC的对象
};

/**
 * 记录客户端的UObject数量
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UObjectTask : public UBaseTask
{
	GENERATED_BODY()
public:
	UObjectTask();
	virtual void InitParam() override;	//解析参数一到参数五
	virtual void TickObject() override;		//tick task
	virtual bool Condition() override;

	//获取此地图上创建的UObject的平均数量
	int32 GetAvgObjCount();	
	int32 GetMinObjCount();
	int32 GetMaxObjCount();

public:
	float LifeTime;		//需要记录的时间
	UPROPERTY(BlueprintReadWrite, Category = "Object")
		TArray<FOBJRECORD> ObjRecords;

};

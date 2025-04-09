// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseTask.h"
#include "FMOTask.generated.h"

/*
* 文件名称：FMOTask.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFMORECORD
{
	GENERATED_USTRUCT_BODY()

public:
	FDateTime Time;
	float FPS;	//FPS
	float UsePhysical; //使用物理内存
	float UseVirtual;	//使用的虚拟内存
	int32 ObjCounts;	//包括不会被GC的CDO对象
	int32 GCObjCount;	//会被GC的对象
};

/**
 * 统计帧率，内存和UObject对象数量
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UFMOTask : public UBaseTask
{
	GENERATED_BODY()
public:
	UFMOTask();
	virtual void InitParam() override;	//解析参数一到参数五
	virtual void TickObject() override;		//tick task
	virtual bool Condition() override;

	//获取此地图上平均帧率
	void GetAvgData(float& AvgFrame, float& AvgMemUse, int32& AvgObjCount);
	void GetMinData(float& MinFrame, float& MinMemUse, int32& MinObjCount);
	void GetMaxData(float& MaxFrame, float& MaxMemUse, int32& MaxObjCount);

	//获取物理内存结果
	FString GetLine();
	static FString GetTitle();

	//获取虚幻内存结果
	FString GetVirtualLine();
	static FString GetVirtualTitle();

	//获取详细结果
	FString GetDetailLine();
	static FString GetDetailTitle();
public:
	float LifeTime;		//需要记录的时间
	FString MapName;	//地图名
	UPROPERTY(BlueprintReadWrite, Category = "Object")
		TArray<FFMORECORD> FMORecords;
	
	
	
};

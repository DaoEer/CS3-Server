// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameData/CsvTableRowBase.h"
#include "GameData/TickObject.h"
#include "AutoTest/AutoTestDebug.h"
#include "BaseTask.generated.h"

/*
* 文件名称：BaseTash.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTASKDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString ClassScript;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		int32 Index;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Param1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Param2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Param3;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Param4;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Param5;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "TaskData")
		FString Comment;
};


/**
 *用于处理自动化测试中的基类任务 
 *
 */

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UBaseTask : public UTickObject
{
	GENERATED_BODY()
	
public:
	UBaseTask();
	void SetParams(const FTASKDATA& TaskData);	//在创建对象之后调用，设置默认参数一到参数五
	void StartTick();		//在开始此task时，开启它的tick功能
	/****		need to override		****/
	virtual void InitParam() {}	//解析参数一到参数五
	virtual void BeginTask() {}	//开始执行task
	virtual void TickObject() override;		//tick task
	virtual bool Condition() { return true; }
	virtual void EndTask() {
		IsComplete = true; bCanEverTick = false; AT_INFO(TEXT("Close TickObject ->Index[%d]"), Index);
	}		//结束执行task
	/****		need to override		****/

public:
	//标记当前任务是否完成
	bool IsComplete; 
	int32 Index;
	FString Param1;
	FString Param2;
	FString Param3;
	FString Param4;
	FString Param5;
	FString Comment;

};

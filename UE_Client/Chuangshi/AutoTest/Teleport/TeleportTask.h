// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "AutoTest/BaseTest/BaseTask.h"
#include "TeleportTask.generated.h"

/*
* 文件名称：TeleportTask.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTeleportTask : public UBaseTask
{
	GENERATED_BODY()
	
public:
	UTeleportTask();
	/****		need to override		****/
	virtual void InitParam() override;	//解析参数一到参数五
	virtual void BeginTask() override;	//开始执行task
	virtual void TickObject() override;		//tick task
	virtual bool Condition() override;
	virtual void EndTask() override;		//结束执行task
	/****		need to override		****/

public:
	FString Position;	//以空格分隔，"0 0 0"
	FString Direction;	//以空格分隔，"0 0 0"
	FString ScriptID;

	
	
};

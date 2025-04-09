// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/TickObject.h"
#include "BaseTask.h"
#include "AutoTest/AutoTestDebug.h"
#include "BaseProfile.generated.h"

/*
* 文件名称：BaseProfile.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UBaseProfile : public UTickObject
{
	GENERATED_BODY()
	
public:
	UBaseProfile();

	//开始执行记录
	void StartRecord();
	virtual void StartTickTask();
	/****		need to override		****/
	virtual void LoadCfg();
	/****		need to override		****/
	virtual void TickObject() override;
	virtual void EndRecord() {}		//一般处理生成csv报告
	bool IsComplete();

	UBaseTask* GetCurrTask();

	
public:
	UPROPERTY()
	TArray<UBaseTask*> Tasks;

	//当前执行到第几个task
	int32 CurrTaskIndex = 0;
	
};

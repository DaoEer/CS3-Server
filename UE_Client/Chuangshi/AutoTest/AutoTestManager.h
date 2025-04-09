// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "AutoTest/BaseTest/BaseProfile.h"
#include "AutoTestManager.generated.h"

/*
* 文件名称：AutoTestManager.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-10-24
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UAutoTestManager : public UObject
{
	GENERATED_BODY()
	
public:
	UAutoTestManager();
	static UAutoTestManager* GetInstance();
	
	UFUNCTION(BlueprintCallable, Category = "AutoTest")
	void StartFMO();

	UFUNCTION(BlueprintCallable, Category = "AutoTest")
		void StopFMO();

	UFUNCTION(BlueprintCallable, Category = "AutoTest")
		void PrintFMO();

public:
	UPROPERTY()
		UBaseProfile* Profile;
	bool bIsStartFMO = false;
	//static UAutoTestManager* Instance;
};

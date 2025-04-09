// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "TrapInterface.h"
#include "TrapBattleFlagInterface.generated.h"

/*
* 文件名称：TrapBattleFlagInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-26
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTrapBattleFlagInterface : public UTrapInterface
{
	GENERATED_BODY()
		typedef UTrapInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UTrapBattleFlagInterface();
	~UTrapBattleFlagInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.TrapBattleFlagInterface'"); } //获取蓝图对象路径
	UFUNCTION(BlueprintCallable, Category = "TrapBattleFlagInterface")
	void OnRep_occurProgress();
	UFUNCTION(BlueprintCallable, Category = "TrapBattleFlagInterface")
	void OnRep_maxProgress();
	UFUNCTION(BlueprintCallable, Category = "TrapBattleFlagInterface")
	void OnRep_barracksBelongType();
};

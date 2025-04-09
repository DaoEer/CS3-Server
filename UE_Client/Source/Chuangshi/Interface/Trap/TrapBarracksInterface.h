// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "TrapBattleFlagInterface.h"
#include "TrapBarracksInterface.generated.h"

/*
* 文件名称：TrapBarracksInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-28
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTrapBarracksInterface : public UTrapBattleFlagInterface
{
	GENERATED_BODY()
		typedef UTrapBattleFlagInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:

	UTrapBarracksInterface();
	~UTrapBarracksInterface();
	static FString GetName() { return TEXT("TrapBarracksInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_TrapBarracksInterface.BP_TrapBarracksInterface_C'"); } //获取蓝图对象路径
		
	UFUNCTION(BlueprintCallable)
		void AddTrap();

	void OnPlayerBeginOverlap();
	void OnPlayerEndOverlap();

	/**
	* BlueprintCallable，请求打开玩家更换部队界面
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable)
	void OpenBarracksArmyWin(const int32& EntityID_);

	UFUNCTION(BlueprintImplementableEvent, Category = "ServerCharacter")
	void OnHideBarracksArmyWin();///<隐藏更换部队界面

};

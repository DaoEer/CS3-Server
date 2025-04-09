// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/AutomaticFightData.h"
#include "AutoFightMar.generated.h"

/*
* 文件名称：AutoFightMar.h
* 功能说明：
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2018-08-28
*/
UCLASS()
class CHUANGSHI_API UAutoFightMar : public UCS3Object
{
	GENERATED_BODY()
	
public:
	static UAutoFightMar* NewInstance();

	static UAutoFightMar* GetInstanceByCS3GameInstance();

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "UAutoFightMar|Event")
		void OnStartAutoAdd_HpMp();

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable, Category = "UAutoFightMar|Event")
		void OnStopAutoAdd_HpMp();
public:
	//-----------------------------------自动战斗事件------------------------------
	//开启自动战斗成功事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event")
		void OnBeginAutomaticFightOver();

	//打断自动战斗成功事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event")
		void OnBreakFightSuccessed(EBreakAutomaticType BreakType, const FName& IDValue);

	//打断自动战斗失败事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event")
		void OnBreakFightFailed(EBreakAutomaticType BreakType, const FName& IDValue);

	//-----------------------------------自动战斗技能快捷栏事件------------------------------
	//添加技能到自动战斗快捷栏事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|SkillList")
		void OnAddSkillOnListOver(int32 SkillKey, int32 NewSkill);

	//通过自动战斗快捷栏Key移除技能事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|SkillList")
		void OnRemoveSkillOnListByKey(int32 SkillKey);

	//通过技能id移除技能事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|SkillList")
		void OnRemoveSkillOnListByValue(int32 RemSkill);

	//自动战斗快捷栏交换技能事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|SkillList")
		void OnExchangeOnSkill(int32 KeyValue1, int32 KeyValue2);

	//-----------------------------------自动战斗物品快捷栏事件------------------------------
	//添加物品到自动战斗物品快捷栏事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|ItemList")
		void OnAddItemOnListOver(int32 ItemKey, int32 NewUID);

	//通过自动战斗物品快捷栏Key移除物品事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|ItemList")
		void OnRemoveItemOnListByKey(int32 ItemKey);

	//通过物品id移除物品事件
	UFUNCTION(BlueprintImplementableEvent, Category = "UAutoFightMar|Event|ItemList")
		void OnRemoveItemOnListByValue(int32 RemItem);

	//-----------------------------------自动战斗设置事件------------------------------
	//自动战斗设置变化事件
	UPROPERTY(BlueprintAssignable, Category = "UAutoFightMar|Event|SettingData")
		FOnChangeAutoFightData OnChangeAutoFightData;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/SaveGame.h"
#include "GameData/AutomaticFightData.h"
#include "LocalAutoFightData.generated.h"

/**
* 文件名称：LocalAutoFightData.h
* 功能说明：
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2018-08-24
*/
UCLASS()
class CHUANGSHI_API ULocalAutoFightData : public USaveGame
{
	GENERATED_BODY()
	
public:
	ULocalAutoFightData();

	virtual void Serialize(FArchive& Ar) override;

	void InitLocalData();

	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData")
	const FString& GetFileName();

	///获取自动战斗技能栏
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData")
	const TMap<int32, int32>& GetSkillList();

	///获取自动战斗技能栏
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData")
	const TMap<int32, int32>& GetItemList();

	///获得自动战斗设置数据
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData")
	FAUTOFIGHTTTING_DATA GetAutoFightSettingData();


	///-------------------------------------自动战斗技能快捷栏----------------------------------
public:
	///添加技能到自动战斗技能快捷栏
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|SkillList|Set")
	bool AddSkillOnList(int32 SkillKey, int32 NewSkill);

	///移除技能通过自动战斗技能栏Key
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|SkillList|Set")
	bool RemoveSkillOnListByKey(int32 SkillKey);

	///移除技能通过技能id
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|SkillList|Set")
	bool RemoveSkillOnListByValue(int32 RemValue);

	///交换技能,从自动战斗技能栏拖到自动战斗技能栏的都用这个
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|SkillList|Set")
	bool ExchangeOnSkill(int32 KeyValue1, int32 KeyValue2);

	///通过技能ID查找自动战斗技能快捷栏是否有该技能
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SkillList")
	bool IsSkillInListByID(int32 SkillID);

	///通过自动战斗技能栏KEY查找是否有该技能
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SkillList")
	bool IsSkillInListByKey(int32 SkillKey);

	///通过自动战斗技能栏Key值获得技能ID
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SkillList")
	const int32 GetSkillByKey(int32 KeyValue);

	///通过技能ID获得自动战斗技能栏Key值
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SkillList")
	const int32 GetKeyBySkill(int32 SkillValue);

	///-------------------------------------自动战斗物品快捷栏----------------------------------
public:
	///添加物品到自动战斗物品快捷栏
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|ItemList|Set")
	bool AddItemOnList(int32 ItemKey, int32 NewID);

	///移除物品通过自动战斗物品栏Key
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|ItemList|Set")
	bool RemoveItemOnListByKey(int32 ItemKey);

	///移除物品通过物品id
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|ItemList|Set")
	bool RemoveItemOnListByValue(int32 RemValue);

	///通过自动战斗物品栏Key值获得物品ID
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|ItemList")
	int32 GetItemIDByKey(int32 KeyValue);

	///通过自动战斗物品栏Key值获得物品ID
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|ItemList")
	int32 GetKeyByItemID(int32 ItemID);

	///通过物品ID查找自动战斗物品快捷栏是否有该物品
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|ItemList")
	bool IsItemInListByID(int32 ItemID);

	///通过自动战斗物品栏KEY查找是否有该物品
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|ItemList")
	bool IsItemInListByKey(int32 ItemlKey);

	///-------------------------------------自动战斗设置----------------------------------
public:
	///设置自动战斗设置数据
	UFUNCTION(BlueprintCallable, Category = "LocalAutoFightData|SettingData|Set")
	void SetAutoFightSettingData(FAUTOFIGHTTTING_DATA data);

	///获得自动战斗默认设置数据
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	FAUTOFIGHTTTING_DATA GetDefultAutoFightSettingData();

	///获取自动战斗范围
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	float GetFightRange();

	///获得某类型拾取类型是否可自动拾取
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	bool CanPickupByType(EAutomaticPickupType type);

	///是否能自动组队
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	bool IsCanAutoJoinTeam();

	///获取可自动拾起物品类型列表
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	const TArray<EAutomaticPickupType> GetCanPickUpList();

	///自动战斗设置数据是否有修改
	UFUNCTION(BlueprintPure, Category = "LocalAutoFightData|SettingData")
	bool CheckAutoFightSettingDataChanged(FAUTOFIGHTTTING_DATA data);
private:
	///设置战斗范围
	void SetFightRange(float NewFightRange);

	///设置HP使用最低百分比
	void SetAddHPPercentage(float Percentage);

	///设置MP使用最低百分比
	void SetAddMPPercentage(float Percentage);


private:
	UPROPERTY(VisibleAnywhere)
	FString FileName;	

public:
	///自动战斗技能快捷栏
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalAutoFightData")
	TMap<int32, int32> SkillList;
	///自动战斗物品快捷栏        血瓶和蓝瓶，KEY为0是血瓶，KEY为1是蓝瓶
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalAutoFightData")
	TMap<int32, int32> ItemOfHPMPList;
	///自动战斗设置
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "LocalAutoFightData")
	FAUTOFIGHTTTING_DATA SettingData;
};

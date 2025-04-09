// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemBase.h"
#include "ItemComposeEquipBP.generated.h"

/*
* 文件名称：ItemComposeEquipBP.h
* 功能说明：绿装打造图纸
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-03-07
*/
UCLASS()
class CHUANGSHI_API UItemComposeEquipBP : public UItemBase
{
	GENERATED_BODY()
	
public:
	virtual FString GetItemName()override;
	/**
	*BlueprintCallable，获取基础属性值
	*
	*@return FString 基础属性
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetAttackPropertyStr();
	/**
	*BlueprintCallable，获取解析propstr后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propcolor 参数颜色
	*
	*@return FString 解析propstr后的值颜色转换成propcolor之后的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		virtual FString ParseMainPropertiesStr(const FString& propstr, const FString& propcolor);

	// 图纸总的成功率
	UFUNCTION(BluePrintCallable)
		float GetTotalSuccessRate();
	// 获取合成装备ID
	UFUNCTION(BluePrintCallable)
		int32 GetComposeEquipID();

	virtual void InitDynamicDataForJson(FString jsonStr) override;

private:
	///<获取属性描述，仅描述字符串，无显示相关转换
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetPropertyStrWithNoColor(const FString& propid, const FString& propvalue);

public:
	// 套装索引（0:没有，1:冰，2:火，3:玄，4:雷）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 suitIndex;
	// 成功率（0~100）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 successRate;
	// 增加的成功率（0~100）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		float addRate;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		FString attackPropertiesStr;///<基础属性
};

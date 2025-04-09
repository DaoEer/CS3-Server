// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/Equip.h"
#include "EquipPart.generated.h"

/*
* 文件名称：EquipPart.h
* 功能说明：半成品装备，需要淬炼才能穿戴
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-03-07
*/
UCLASS()
class CHUANGSHI_API UEquipPart : public UEquip
{
	GENERATED_BODY()

	typedef UEquip Super;
public:
	/**
	*虚函数，是否可以使用物品
	*
	*@return bool 可以使用物品返回TRUE，否则返回FALSE
	*/
	virtual bool IsCanUse() override;
	
	virtual FString GetItemName()override;

	/**
	*virtual，获取附加属性值
	*
	*@return FString 附加属性值
	*/
	virtual FString GetAttachPropertyStr() override;

	virtual void InitDynamicDataForJson(FString jsonStr) override;

	//淬炼
	void OnQuenching();
public:
	// 淬炼次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 quenchingNum;
	
};

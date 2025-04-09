// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemBase.h"
#include "ItemJadeCommond.generated.h"



/**
* 文件名称：ItemJadeCommond.h
* 功能说明：玲珑玉令脚本
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-03-31
*/
UCLASS()
class CHUANGSHI_API UItemJadeCommond : public UItemBase
{
	GENERATED_BODY()

public:
	virtual void InitDynamicDataForJson(FString jsonStr) override;

	// 玲珑玉令等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 jadeLevel;
	// 是否有效
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 isValid;
	
};

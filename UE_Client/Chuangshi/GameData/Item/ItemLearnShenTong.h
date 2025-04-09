// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemUse.h"
#include "ItemLearnShenTong.generated.h"

/*
* 文件名称：ItemLearnShenTong.h
* 功能说明：学习神通技能道具
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-08-24
*/
UCLASS()
class CHUANGSHI_API UItemLearnShenTong : public UItemUse
{
	GENERATED_BODY()
		typedef UItemUse Supper;
public:




	virtual void InitDynamicDataForJson(FString jsonStr) override;

public:
	// 充能次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemLearnShenTong | Property")
		int32 UseTimes;
	
};

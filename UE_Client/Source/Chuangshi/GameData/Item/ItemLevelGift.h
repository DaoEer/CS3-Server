// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemUse.h"
#include "ItemLevelGift.generated.h"

class AServerCharacter;
/**
* 文件名称：ItemLevelGift.h
* 功能说明：
* 文件作者：kangyan
* 目前维护：kangyan
* 创建时间：2019-10-23
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UItemLevelGift : public UItemUse
{
	GENERATED_BODY()
public:
	virtual void InitDynamicDataForJson(FString jsonStr) override;
	virtual int32 Use(AServerCharacter* player) override;

};
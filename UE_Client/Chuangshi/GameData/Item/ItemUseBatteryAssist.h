// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemUseAssist.h"
#include "ItemUseBatteryAssist.generated.h"

/**
* 文件名称：ItemUseAssist.h
* 功能说明：表现右键使用物品，出现半透明模型作为施法辅助（功能对位置施法）
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-03-30
*/
class AServerCharacter;

UCLASS()
class CHUANGSHI_API UItemUseBatteryAssist : public UItemUseAssist
{
	GENERATED_BODY()
	

public:
	// 施法辅助模型 朝向
	virtual FRotator GetModelRotationAssist(const AServerCharacter* Owner) override;
	// 检查施法辅助 有效性
	virtual bool CheckModelAssistValid(const FVector& Pos) override;
};

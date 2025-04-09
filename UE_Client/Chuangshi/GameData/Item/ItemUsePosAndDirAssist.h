// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemUseAssist.h"
#include "ItemUsePosAndDirAssist.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UItemUsePosAndDirAssist : public UItemUseAssist
{
	GENERATED_BODY()
	

public:
	virtual bool IsUseItemToPosition() override { return true; };
	virtual bool IsUseDirection() override { return true; };

	// 施法辅助模型 朝向
	virtual FRotator GetModelRotationAssist(const AServerCharacter* Owner) override { return FRotator::ZeroRotator; };

};

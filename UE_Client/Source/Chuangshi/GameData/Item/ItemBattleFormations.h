// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Item/ItemBase.h"
#include "ItemBattleFormations.generated.h"



/**
* 文件名称：ItemBattleFormations.h
* 功能说明：图阵
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-05-14
*/
UCLASS()
class CHUANGSHI_API UItemBattleFormations : public UItemBase
{
	GENERATED_BODY()

public:
	// 获取图阵血量
	UFUNCTION(BlueprintPure)
		FString GetBattleFormationsHP();
		
	// 获取每分钟消耗 和 激活消耗
	UFUNCTION(BluePrintCallable)
		void GetPerAndTotalSoume(int32& PerSoume, int32& TotalSoume);
};

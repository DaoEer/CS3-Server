// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "StallItemData.generated.h"

/**
* 文件名称：StallItemData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-03-23
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FStallItemData
{
	GENERATED_USTRUCT_BODY()
		FStallItemData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "id")
		FString Id;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "itemID")
		int32 ItemID = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "amount")
		int32 Amount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "price")
		int32 Price = 0;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "ItemType.generated.h"

/**
* 文件名称：ItemType.h
* 功能说明：物品类型分类配置表
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FItemType : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		//FItemType() {}
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemType")
		FString StrType;
	
};
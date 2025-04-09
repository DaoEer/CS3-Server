// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "FactionRelationData.generated.h"

/**
* 文件名称：FactionRelationData.h
* 功能说明：势力关系结构体
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-04-17
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FFACTION_RELATION_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	/** 势力1 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 FactionA = 0;
	/** 势力2 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 FactionB = 0;
	/** 关系：敌对填1；友好填0 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Relation = 0;
};

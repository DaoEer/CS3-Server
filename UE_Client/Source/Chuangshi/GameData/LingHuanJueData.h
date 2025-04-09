// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "LingHuanJueData.generated.h"

/**
* 文件名称：LingHuanJueData.h
* 功能说明：
* 文件作者：fangpengjun
* 目前维护：fangpengjun
* 创建时间：2020-04-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLINGHUANJUE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///每个难度有多组，每组有多个格子
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FLINGHUANJUE_DATA", DisplayName = "GroupID")
		int32  GroupID;
	///格子索引
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FLINGHUANJUE_DATA", DisplayName = "LatticeIndex")
		int32 LatticeIndex;
		///难度
		UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FLINGHUANJUE_DATA", DisplayName = "Difficulty")
		int32 Difficulty;
	///格子中第一个指针初始化索引
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FLINGHUANJUE_DATA", DisplayName = "PointerIndex")
		int32 PointerIndex;
	///夹角，大于0表示有2个指针,等于0表示只有1个指针
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "FLINGHUANJUE_DATA", DisplayName = "PointerAngle")
		float PointerAngle = 0.0;
};

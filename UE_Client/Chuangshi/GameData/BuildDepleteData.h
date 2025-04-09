// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "BuildDepleteData.generated.h"

/**
* 文件名称：BuildDepleteData.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-13
*/

///建筑消耗
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBULID_DEPLETE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 灵泉
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "LingQuan")
		TMap<int32, int32> lingQuan;
	//工坊
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "GongFang")
		TMap<int32, int32>  gongFang;
	//乾坤鼎
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "QianKuDing")
		TMap<int32, int32>  qianKuDing;
	//兽栏
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "ShouLan")
		TMap<int32, int32>  shouLan;
	//灵田
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "LingTian")
		TMap<int32, int32> lingTian;
	// 升级需要的金钱（灵泉|工坊|乾坤鼎|兽栏|灵田）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "BuildDepleteMoney")
		TMap<int32, int32> buildDepleteMoney;
	// 升级需要的灵能（灵泉|工坊|乾坤鼎|兽栏|灵田）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "BuildDepletePsionic")
		TMap<int32, int32> buildDepletePsionic;
	// 升级需要的时间（灵泉|工坊|乾坤鼎|兽栏|灵田）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BuildData", DisplayName = "BuildDepleteTime")
		TMap<int32, int32> buildDepleteTime;
	
};
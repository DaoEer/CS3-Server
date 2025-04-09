// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "TeleportPointData.generated.h"

/**
* 文件名称：TeleportPointData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-11-17
*/

/** 传送点 */
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTELEPORT_POINT_DATA :public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//地图名
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ScriptID")
		FString ScriptID;
	//客户端位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Position")
		FVector Position;
	//客户端朝向
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Direction")
		FVector Direction;
	//等级限制
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "LimitLevel")
		int32 LimitLevel = 0;
	//阵营限制
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "LimitCamp")
		int32 LimitCamp = 0;
	//金钱消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MoneyCost")
		int32 MoneyCost = 0;
	//传送目的地名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DstName")
		FString DstName;
	//传送目的地NPC
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DstNPCID")
		FString DstNPCID;
	//传送点描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Describe")
		FString Describe;
	//传送点是否默认开启
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "IsOpen")
		bool IsOpen;
};
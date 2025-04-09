// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "TrainSoldierGroundAreaCfg.generated.h"


/**
* 文件名称：TrainSoldierGroundAreaCfg.h
* 功能说明：练兵场区域配置表 JIRA CST-11218
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-6-29
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTrainSoldierGroundNpcData
{
	GENERATED_USTRUCT_BODY()
public:
	///NPC索引，唯一标识符
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Group;
	///NPC脚本ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///NPC类型 (1:初级2:中级3:高级)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TrainGroundType;
	///NPC名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	///NPC位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	///传送位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector TeleportPosition;
};
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTRAIN_SOLDIER_GROUND_MAP_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///区域索引，唯一标识符
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Index;
	///区域名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	///区域里所有练兵场
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTrainSoldierGroundNpcData> TrainSoldierGroundNpcData;
	///区域中心点
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector CenterPosition;
	///区域范围
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FVector> Polygon;
};

// 兵营 据点等信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTG_BARRACK
{
	GENERATED_USTRUCT_BODY()
public:
	///NPC脚本ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///归宿攻守方（0：进攻方，1：防守方）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BelongSide;
	///NPC位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
};

// 器械等信息
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTG_BATTERY
{
	GENERATED_USTRUCT_BODY()
public:
	/// entityID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 EntityID;
	///NPC脚本ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///状态（0：已被摧毁，1：正常状态）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 State;
	///NPC位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
};
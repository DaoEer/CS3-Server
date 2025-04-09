// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BarracksSoldierPropertyData.generated.h"

/**
* 文件名称：BarracksSoldierPropertyData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-28
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_SOLDIER_PROPERTY_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///兵ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ScriptID")
		FString ScriptID;
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Level")
		int32 Level = 0;
	///攻击力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Damage")
		int32 Damage = 0;
	///防御力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Armor")
		int32 Armor = 0;
	///移动速度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MoveSpeed")
	float MoveSpeed = 0.0;
	///攻击距离
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "AttackRange")
	float AttackRange = 0.0;
	///最大生命值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HP_Max")
	int32 HPMax = 0;
};
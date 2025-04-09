// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BarracksGuardSoldierSkillData.generated.h"

/**
* 文件名称：BarracksGuardSoldierSkillData.h
* 功能说明：兵的技能升级数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-30
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_GUARD_SOLDIER_SKILL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///兵ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ScriptID")
	FString ScriptID;
	///兵技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CurrentSkillID")
	int32 CurrentSkillID = 0;
	///下一个兵技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NextLevelSkillID")
	int32 NextLevelSkillID = 0;
	///消耗的经验
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ReqExp")
	int32 ReqExp = 0;
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Level")
	int32 Level = 0;
	///技能名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SkillName")
	FString SkillName;
	///技能图标路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Icon")
	TSoftObjectPtr<UTexture2D> Icon;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Description")
	FString Description = "";
};
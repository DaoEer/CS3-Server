#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "CombatDamager.generated.h"

/**
* 文件名称：CombatDamager.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-08-21
*/


//基准伤害值表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOMBAT_DAMAGER_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 Level = 0;
	///玩家职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 Profession = 0;
	///伤害波动
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		float DamRandom = 0;
	///基准暴击点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 BCritPoint = 0;
	///基准暴击倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		float BCritRatio = 0;
	///基准招架点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 BParryPoint = 0;
	///基准招架倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		float BParryRatio = 0;
	///基准防御点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 BArmorPoint = 0;
	///基准罡气防御点
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 GangQiArmorPoint = 0;
	///自然仇恨下限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 HatredLL = 0;
	///自然连带仇恨下限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 RelatedHatredLL = 0;
	///自然仇恨倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		float HatredRatio = 0;
	///自然连带仇恨倍率
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		float RelatedHatredRatio = 0;
	///基准仇恨
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 BHatred = 0;
	///基准连带仇恨
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CombatDamager")
		int32 BRelatedHatred = 0;
};
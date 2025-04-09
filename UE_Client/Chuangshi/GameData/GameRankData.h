// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatType.h"
#include "GameRankData.generated.h"

/**
* 文件名称：GameRankData.h
* 功能说明：游戏排行榜
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-09-03
*/

UENUM(Blueprintable)
enum class EGameRank : uint8
{
	///等级排行榜
	Level_Rank = 0,
	///战力排行榜
	Combat_Rank,
	///财富排行榜
	Money_Rank,
	///神器排行榜
	Weapon_Rank,
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLevelRankData
{
	GENERATED_USTRUCT_BODY()
		FLevelRankData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerDBID")
		FString playerDBID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerName")
		FString playerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "camp")
		int32 camp = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "profession")
		int32 profession = 0;
	// 战斗力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "combatPower")
		int32 combatPower = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
		int32 level = 0;
	// 名次升降（负数为降）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ascend")
		int32 ascend = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCombatRankData : public FLevelRankData
{
	GENERATED_USTRUCT_BODY()
		FCombatRankData() {};
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMoneyRankData
{
	GENERATED_USTRUCT_BODY()
		FMoneyRankData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerDBID")
		FString playerDBID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerName")
		FString playerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "camp")
		int32 camp = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "profession")
		int32 profession = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "money")
		int64 money;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
		int32 level = 0;
	// 名次升降（负数为降）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ascend")
		int32 ascend = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FWeaponRankData
{
	GENERATED_USTRUCT_BODY()
		FWeaponRankData() {};
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerDBID")
		FString playerDBID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playerName")
		FString playerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "camp")
		int32 camp = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "weaponUID")
		FString weaponUID;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "weaponID")
		int32 weaponID = 0;
	// 品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "quality")
		int32 quality = 0;
	// 战斗力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "combatPower")
		int32 combatPower = 0;
	// 装备属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "attackProperties")
		FString attackProperties;
	// 装备附加属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "attachProperties")
		FString attachProperties;
	// 装备强化属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "intensifyProperties")
		FString intensifyProperties;

	// 名次升降（负数为降）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ascend")
		int32 ascend = 0;
};
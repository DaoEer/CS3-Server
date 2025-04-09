// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ModifyFaceData.h"
#include "RoleInfo.generated.h"


/**
* 文件名称：RoleInfo.h
* 功能说明：角色信息
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-7-11
*/

USTRUCT(BlueprintType)
struct FROLEINFO {
	GENERATED_USTRUCT_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString dbid;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString playerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 profession = 0;//职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 camp = 0;//阵营(1仙道 2魔道)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gender = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString offlineTime;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> bonenames;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> bonedatas;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FFACE_STYLE_DATA facestyledata;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Index;//索引1-8
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ModelID;//模型ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsAccount;
};

/// 玩家查看信息
USTRUCT(BlueprintType)
struct FROLEPROPERTYINFO {
	GENERATED_USTRUCT_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 profession = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 camp = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gender = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xiuwei = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 jingjieLevel = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 killingValue = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 feats = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 potential = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 combatPower = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 strength = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 dexterity = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 intellect = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 corporeity = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 discern = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 speed = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 HP = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 HP_Max = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MP = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MP_Max = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gangQiValue = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gangQiValue_Max = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 magic_damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 cure = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 magic_armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gangQi_damagePoint = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 gangQi_armorPoint = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 criticalstrike = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 parry = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 hitrate = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 dodgerate = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 healingrate = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ice_damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 fire_damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 thunder_damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xuan_damage = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ice_armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 fire_armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 thunder_armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xuan_armor = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 magic_damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 magic_armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 criticalstrike_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 parry_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 hitrate_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 dodgerate_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ice_damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 fire_damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 thunder_damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xuan_damage_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ice_armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 fire_armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 thunder_armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 xuan_armor_ignore = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 depress_resist = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 hitback_resist = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 control_resist = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 insane_resist = 0;
};
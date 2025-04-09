// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "RoleCreateUIData.generated.h"

/**
* 文件名称：RoleCreateUIData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2016-10-14
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleCreateUIData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FRoleCreateUIData() {};
public:
	///PC演示人模型（@DT_ModelCfg）
	///	用于：创建角色\选择角色\角色面板
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RoleModelName")
		FName RoleModelName;

	///PC标准人模型（@DT_ModelCfg）
	///	用于：游戏场景
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RoleGameModelName")
		FName RoleGameModelName;
	
	///阵营
	///	1＝仙道（@csdefine.阵营）
	///	2＝魔道
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RoleCamp")
		int32 RoleCamp = 0;

	///职业
	///	1＝战士（@csdefine.职业）
	///	2＝剑客
	///	3＝射手
	///	4＝法师
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RoleProfession")
		int32 RoleProfession = 0;

	///性别
	///	1＝男（@csdefine.性别）
	///	2＝女
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RoleGender")
		int32 RoleGender = 0;

	///职业名称显示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ProfessionName")
		FName ProfessionName;

	///创建角色关卡名（四个职业有四个关卡）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "LevelCreateName")
		FString LevelCreateName;

	///创建角色关卡中的角色位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Position")
		FTransform Position;

	///创建角色摄像机ID（@DT_SpawnTransformCfg）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SpawnCameraId")
		FString SpawnCameraId;

};
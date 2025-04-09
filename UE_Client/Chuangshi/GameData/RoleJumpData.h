// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "RoleJumpData.generated.h"

///跳跃时空中飞行类型
UENUM(BlueprintType)
enum class JUMP_SHOW_TYPE : uint8
{
	JUMP_SHOW_NULL = 0 UMETA(DisplayName = "JUMP_SHOW_NULL"),
	JUMP_SHOW_PAOWUXIAN = 1 UMETA(DisplayName = "JUMP_SHOW_PAOWUXIAN"),//抛物线
	JUMP_SHOW_YUNSU = 2 UMETA(DisplayName = "JUMP_SHOW_YUNSU"),//匀速
	JUMP_SHOW_ACTION = 3 UMETA(DisplayName = "JUMP_SHOW_ACTION"),//动作
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCHARACTER_MOVE_CACHE_DATA : public FTableRowBase
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(BlueprintReadOnly, Category = "RoleData", DisplayName = "GravityScale")
		float GravityScale;
	UPROPERTY(BlueprintReadOnly, Category = "RoleData", DisplayName = "MaxAcceleration")
		float MaxAcceleration;
	UPROPERTY(BlueprintReadOnly, Category = "RoleData", DisplayName = "BrakingDecelerationFalling")
		float BrakingDecelerationFalling;//横向减速度
	UPROPERTY(BlueprintReadOnly, Category = "RoleData", DisplayName = "MaxWalkSpeed")
		float MaxWalkSpeed;
	UPROPERTY(BlueprintReadOnly, Category = "RoleData", DisplayName = "JumpZVelocity")
		float JumpZVelocity;
};
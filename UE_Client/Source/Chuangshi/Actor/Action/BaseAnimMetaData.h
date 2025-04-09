// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
//UE4
#include "Animation/AnimMetaData.h"
#include "BaseAnimMetaData.generated.h"

/// 动作结束的中断类型
UENUM(BlueprintType)
enum class ACTION_INTERRUPTED_ENUM : uint8
{
	ACTION_INTERRUPTED_STOP = 1 UMETA(DisplayName = "RoleProfessionZhanShi"),//蒙太奇停止
	ACTION_INTERRUPTED_OTHER = 2 UMETA(DisplayName = "RoleProfessionJianKe"),//其他中断
};

/*
* 文件名称：BaseAnimMetaData.h
* 功能说明：动作对象元数据，用作标识数据绑定到动作对象里
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-07-24
*/
UCLASS()
class CHUANGSHI_API UBaseAnimMetaData : public UAnimMetaData
{
	GENERATED_BODY()
public:
	void SetInterruptedType(ACTION_INTERRUPTED_ENUM InInterruptedType);
	ACTION_INTERRUPTED_ENUM GetInterruptedType();

private:
	ACTION_INTERRUPTED_ENUM InterruptedType;
	
};

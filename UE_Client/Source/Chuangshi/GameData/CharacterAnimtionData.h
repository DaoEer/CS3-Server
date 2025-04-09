// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CharacterAnimtionData.generated.h"

/**
* 文件名称：CharacterAnimData.h
* 功能说明：人物动作数据
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2018-12-19
*/

///动作融合类型枚举
UENUM(BlueprintType)
enum class ANIM_BLEND_TYPE_ENUM : uint8
{
	ANIM_BLEND_ROOT = 0 UMETA(DisplayName = "DefaultSlot"),///<根节点融合
	ANIM_BLEND_BODY = 1 UMETA(DisplayName = "SlotBody01"),///<半身融合
	ANIM_BLEND_FACE = 2 UMETA(DisplayName = "SlotFace01"),///<表情融合
};
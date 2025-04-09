// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatPageType.generated.h"

/**
* 文件名称：ChatPageType.h
* 功能说明：
* 文件作者：ouyangminzhen
* 目前维护：hejingke
* 创建时间：2016-11-18
*/
UENUM(BlueprintType)
enum class ChatPageType : uint8
{
	/// 综合
	Synthesis UMETA(DisplayName = "Synthesis"),
	/// 常用
	Common UMETA(DisplayName = "Common"),
	/// 其它
	Other UMETA(DisplayName = "Other"),
	/// 密语
	Private UMETA(DisplayName = "Private"),
	/// 战斗
	Fight UMETA(DisplayName = "Fight"),
	/// 自定义1
	Custom1 UMETA(DisplayName = "Custom1"),
	/// 自定义2
	Custom2 UMETA(DisplayName = "Custom2"),

};

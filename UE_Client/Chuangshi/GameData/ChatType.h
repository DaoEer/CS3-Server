// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "ChatType.generated.h"

/**
* 文件名称：ChatType.h
* 功能说明：
* 文件作者：huangshijie
* 目前维护：hejingke
* 创建时间：2016-09-06
*/

UENUM(BlueprintType)
enum class ChatType : uint8
{
	/// 附近
	Nearby UMETA(DisplayName = "Nearby"),
	/// 地图
	Space UMETA(DisplayName = "Space"),
	/// 世界
	World UMETA(DisplayName = "World"),
	/// 密语
	Whisper UMETA(DisplayName = "Whisper"),
	/// 讨论组
	Group UMETA(DisplayName = "Group"),
	/// 队伍
	Team UMETA(DisplayName = "Team"),
	/// 团队
	Collective UMETA(DisplayName = "Collective"),
	/// 帮会
	Gang UMETA(DisplayName = "Gang"),
	/// 联盟
	Aliance UMETA(DisplayName = "Aliance"),
	/// 门派
	School UMETA(DisplayName = "School"),
	/// 阵营
	Camp UMETA(DisplayName = "Camp"),
	/// 战场
	Battlespace UMETA(DisplayName = "Battlespace"),
	/// 天音
	Tianyin UMETA(DisplayName = "Tianyin"),
	/// 仙音
	Xianyin UMETA(DisplayName = "Xianyin"),
	/// 系统
	System UMETA(DisplayName = "System"),
	/// 朋友
	Friend UMETA(DisplayName = "Friend"),
};

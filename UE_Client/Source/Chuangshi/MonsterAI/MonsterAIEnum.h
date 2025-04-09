#pragma once
#include "UObject/ObjectMacros.h"

UENUM(BlueprintType)
enum class MONSTER_AI_EVENT : uint8
{
	///有玩家进入当前客户端
	ROLE_ENTER_WORLD = 0 UMETA(DisplayName = "ROLE_ENTER_WORLD"),
	///有怪物进入当前客户端
	MONSTER_ENTER_WORLD = 1 UMETA(DisplayName = "MONSTER_ENTER_WORLD"),
};

UENUM(BlueprintType)
enum class MONSTER_AI_COMMAND : uint8
{
	///指令
	NONE = 0 UMETA(DisplayName = "NONE"),
	///跟随指令
	FOLLOW = 1 UMETA(DisplayName = "FOLLOW"),
	///列阵 
	FORMATION = 2 UMETA(DisplayName = "FORMATION"),
	///攻击指令
	ATTACK = 3 UMETA(DisplayName = "ATTACK"),
	///攀爬指令
	CLIMB = 4 UMETA(DisplayName = "CLIMB"),
	
};

enum class MONSTER_AI_COMMAND_PROCESS : uint8
{
	///指令
	READY = 0 UMETA(DisplayName = "READY"),
	///跟随指令
	PROCESS = 1 UMETA(DisplayName = "PROCESS"),
	///攻击指令
	OVER = 2 UMETA(DisplayName = "OVER"),
};

UENUM(BlueprintType)
enum class MONSTER_AI_STATE : uint8
{
	///死亡状态
	DEAD = 0 UMETA(DisplayName = "DEAD"),
	///普通状态
	NORMAL = 1 UMETA(DisplayName = "NORMAL"),

	ESCAPE = 2 UMETA(DisplayName = "ESCAPE"),
};

UENUM(BlueprintType)
enum class MONSTER_AI_MOVETYPE : uint8
{
	Stop			= 0 UMETA(DisplayName = "Stop"),
	MoveToPos		= 1 UMETA(DisplayName = "MoveToPos"),
	MoveChaseActor	= 2 UMETA(DisplayName = "MoveChaseActor"),
	MoveCharge		= 3 UMETA(DisplayName = "MoveCharge"),
	MoveMarch		= 4 UMETA(DisplayName = "MoveMarch"),
	MoveFollow		= 5 UMETA(DisplayName = "MoveFollow"),
	MoveRect		= 6	UMETA(DisplayName = "MoveRect"),
	MoveCircle      = 7	UMETA(DisplayName = "MoveCircle"),

};

///阵型
UENUM(BlueprintType)
enum class MONSTER_AI_FORMATION : uint8
{
	///矩形
	Rectangle = 1 UMETA(DisplayName = "Rectangle"),

	///圆形
	Circle = 2 UMETA(DisplayName = "Circle"),
};

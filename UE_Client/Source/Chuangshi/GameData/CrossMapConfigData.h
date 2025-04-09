#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "CrossMapConfigData.generated.h"

/**
* 文件名称：CrossMapConfigData.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-11-24
*/

UENUM(BlueprintType)
enum class ENUM_CROSS_MAP_TELEPORT_TYPE : uint8
{
	///TeleportDefault（默认不需要传送的类型）
	TeleportDefault = 0 UMETA(DisplayName = "TeleportDefault"),
	///TeleportNPC（NPC）
	TeleportNPC = 1 UMETA(DisplayName = "TeleportNPC"),
	///TeleportTrap（Trap）
	TeleportTrap = 2 UMETA(DisplayName = "TeleportTrap"),
	///TeleportSpaceDoor（传送门）
	TeleportSpaceDoor = 3 UMETA(DisplayName = "TeleportSpaceDoor"),
	//TeleportCarter(车夫)
	TeleportCarter = 4 UMETA(DisplayName = "TeleportCarter"),
	///TeleportStone（传送点）
	TeleportPoint = 5 UMETA(DisplayName = "TeleportPoint"),
};

//传送点传送方式
UENUM(BlueprintType)
enum class ENUM_POINT_TELEPORT_TYPE : uint8
{
	///TeleportStone（通过神行石传送）
	TELEPORT_BY_TELEPORTSTONE = 0 UMETA(DisplayName = "TeleportStone"),
	///TeleportMoney（通过消耗金钱传送）
	TELEPORT_BY_MONEY = 1 UMETA(DisplayName = "TeleportMoney"),
	///TeleportUnconditional（无条件(指消耗或神行石)传送）
	TELEPORT_BY_NONE = 2 UMETA(DisplayName = "TeleportUnconditional"),
	///TeleportUnconditional（默认）
	TELEPORT_BY_DEFAULT = 3 UMETA(DisplayName = "TeleportDefault"),
};

//寻路类型，用于区分寻路到达终点后要做的事
UENUM(BlueprintType)
enum class ENUM_NAVIGATE_ACTION_TYPE : uint8
{
	///默认寻路类型，寻路到终点后不做任何事
	NavigateActionDefault = 0 UMETA(DisplayName = "NavigateActionDefault"),
	///摆摊寻路
	NavigateActionStall = 1 UMETA(DisplayName = "NavigateActionStall"),
	///活动寻路
	NavigateActionCrond = 2 UMETA(DisplayName = "NavigateActionCrond")
};

//神行石传送类型
UENUM(BlueprintType)
enum class ENUM_STONE_TELEPORT_TYPE : uint8
{
	///默认传送类型
	StoneTeleportTypeDefault = 0 UMETA(DisplayName = "StoneTeleportTypeDefault"),
	///寻路传送
	StoneTeleportTypeNavigate = 1 UMETA(DisplayName = "StoneTeleportTypeNavigate"),
	///大地图传送
	StoneTeleportTypeBigMap = 2 UMETA(DisplayName = "StoneTeleportTypeBigMap"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_TARGET_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpaceName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;

	FORCEINLINE bool operator==(const FCROSS_MAP_TARGET_INFO& Other) const
	{
		if (this->SpaceName == Other.SpaceName && this->TeleportType == Other.TeleportType \
			&& this->Position == Other.Position && this->ScriptID == Other.ScriptID \
			&& this->Param1 == Other.Param1 && this->Param2 == Other.Param2 \
			&& this->Param3 == Other.Param3)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_QUEST_TARGET_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCROSS_MAP_TARGET_INFO TargetInfo;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsCompletedQuest;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString QuestTaskClass;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 AutoQuestID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 GossipWithType = 0;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSSMAP_TELEPORT_POINT_PARAM
{
	GENERATED_BODY()
public:
	///传送点index
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TeleportIndex;
	///传送石传送后的位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector TeleportPos;
	///传送石所需阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LimitCamp = 0;
	///传送石等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LimitLevel = 0;
	FORCEINLINE bool operator==(const FCROSSMAP_TELEPORT_POINT_PARAM& Other) const
	{
		if (this->TeleportIndex == Other.TeleportIndex && this->TeleportPos == Other.TeleportPos \
			&& this->LimitCamp == Other.LimitCamp && this->LimitLevel == Other.LimitLevel)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSSMAP_SPACEDOOR_PARAM
{
	GENERATED_BODY()
public:
	///传送门ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///传送门所在位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	///传送后的位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector TeleportPos;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSSMAP_NPC_PARAM
{
	GENERATED_BODY()
public:
	///NPC的ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///NPC所在位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	///对应的talk的key
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TalkKey;
	///传送后的位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector TeleportPos;
	///需要的阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;

	FORCEINLINE bool operator==(const FCROSSMAP_NPC_PARAM& Other) const
	{
		if (this->ScriptID == Other.ScriptID && this->Position == Other.Position \
			&& this->TalkKey == Other.TalkKey && this->TeleportPos == Other.TeleportPos
			&& this->Camp == Other.Camp)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSSMAP_TRAP_PARAM
{
	GENERATED_BODY()
public:
	///陷阱的ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///陷阱所在位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_TELEPORT_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSSMAP_TELEPORT_POINT_PARAM> TeleportPointInfos;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCROSSMAP_SPACEDOOR_PARAM SpaceDoorInfo;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSSMAP_NPC_PARAM> NPCInfos;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FCROSSMAP_TRAP_PARAM TrapInfo;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSSMAP_NPC_PARAM> CarterInfos;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_START_TO_END_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StartSpace;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EndSpace;

	FORCEINLINE friend uint32 GetTypeHash(const FCROSS_MAP_START_TO_END_INFO& StartToEndInfo)
	{
		FString HashStr = StartToEndInfo.StartSpace + TEXT("_") + StartToEndInfo.EndSpace;
		return FCrc::Strihash_DEPRECATED(*HashStr);
	}
	FORCEINLINE bool operator==(const FCROSS_MAP_START_TO_END_INFO& Other) const
	{
		if (this->StartSpace == Other.StartSpace && this->EndSpace == Other.EndSpace)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_TARGET_PARAM_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector TargetPosition;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
	
	FORCEINLINE bool operator==(const FCROSS_MAP_TARGET_PARAM_INFO& Other) const
	{
		if (this->TargetPosition == Other.TargetPosition && this->Param1 == Other.Param1 \
			&& this->Param2 == Other.Param2 && this->Param3 == Other.Param3)
		{
			return true;
		}
		else
		{
			return false;
		}
	}

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSS_MAP_TARGET_PARAM_INFO> TargetParam;
	FORCEINLINE bool operator==(const FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO& Other) const
	{
		if (this->Position == Other.Position && this->ScriptID == Other.ScriptID \
			&& this->TargetParam == Other.TargetParam)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSS_MAP_SCRIPTID_TO_TARGET_PARAM_INFO> ScriptIDToTargetInfo;
	FORCEINLINE bool operator==(const FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO& Other) const
	{
		if (this->TeleportType == Other.TeleportType && this->ScriptIDToTargetInfo == Other.ScriptIDToTargetInfo)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_SPACE_TARGET_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpaceName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FCROSS_MAP_TELEPORT_TYPE_TO_TARGET_INFO> TeleportTypeToTargetInfo;

	FORCEINLINE bool operator==(const FCROSS_MAP_SPACE_TARGET_INFO& Other) const
	{
		if (this->SpaceName == Other.SpaceName && this->TeleportTypeToTargetInfo == Other.TeleportTypeToTargetInfo)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FCROSS_MAP_CONFIG_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///当前地图名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString CurrentSpace;
	///目标地图名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DstSpace;
	///传送类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TeleportType;
	///传送的entity的ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ScriptID;
	///备注
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Note;
	///参数1
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数2
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数3
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNAVIGATE_NPC_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SpaceName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString NPCScriptID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsSearch;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float NearbyRange;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector DstPosition;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 AutoQuestID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 GossipWithType = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_CROSS_MAP_TELEPORT_TYPE TeleportType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		ENUM_POINT_TELEPORT_TYPE PointTeleportType;
	///参数1
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///参数2
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///参数3
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;

	FORCEINLINE void ResetData()
	{
		SpaceName = "";
		NPCScriptID = "";
		IsSearch = false;
		NearbyRange = 0.0f;
		AutoQuestID = 0;
		TeleportType = ENUM_CROSS_MAP_TELEPORT_TYPE::TeleportDefault;
		PointTeleportType = ENUM_POINT_TELEPORT_TYPE::TELEPORT_BY_DEFAULT;
		Param1 = "";
		Param2 = "";
		Param3 = "";
		GossipWithType = 0;
	}
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FMAP_RELATED_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MapScriptID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString AreaType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool ForbidUseTeleportPoint;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BHZBData.generated.h"



/**
* 文件名称：BHZBData.h
* 功能说明：帮会争霸数据
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-04-08
*/
UENUM(BlueprintType)
enum class NPCEXTPOINT_TYPE : uint8
{
	///低级据点
	NPCEXTPOINT_TYPE_LOWER_LEVEL = 1 UMETA(DisplayName = "NPCEXTPOINT_TYPE_LOWER_LEVEL"),
	///中级据点
	NPCEXTPOINT_TYPE_MIDDLE_LEVEL = 2 UMETA(DisplayName = "NPCEXTPOINT_TYPE_MIDDLE_LEVEL"),
};

UENUM(BlueprintType)
enum class NPCEXTPOINT_STATE : uint8
{
	///已被宣战
	NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE = 0 UMETA(DisplayName = "NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE"),
	///可被宣战
	NPCEXTPOINT_STATE_CAN_BE_DECLARE = 1 UMETA(DisplayName = "NPCEXTPOINT_STATE_CAN_BE_DECLARE"),
	///争夺中
	NPCEXTPOINT_STATE_FIGHT = 2 UMETA(DisplayName = "NPCEXTPOINT_STATE_FIGHT"),
	///休整中
	NPCEXTPOINT_STATE_REST = 3 UMETA(DisplayName = "NPCEXTPOINT_STATE_REST"),
	///布防中
	NPCEXTPOINT_STATE_DEFENSE = 4 UMETA(DisplayName = "NPCEXTPOINT_STATE_DEFENSE"),
};


USTRUCT(BlueprintType)
struct FBHZBSIGNMEMBERDATA {
	GENERATED_USTRUCT_BODY()
	/// SignID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 SignID = 0;
	/// GroupID 分组
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 GroupID = 0;
	/// CaptainDBID 队长DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString CaptainDBID;
	/// MemberDBIDs 成员DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TArray<FString> MemberDBIDs;
	/// 是否进入争夺地图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool IsActive = false;
	/// 争夺的据点编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PointIndex = 0;
};

USTRUCT(BlueprintType)
struct FBHZBTONGINTEGRALDATA {
	GENERATED_USTRUCT_BODY()
	/// 帮会DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString TongDBID = "";
	/// 帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName = "";
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongLevel = 0;
	/// 占领据点数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 OccupyPointAmount = 0;
	/// 帮会积分
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Integral = 0;
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
};

USTRUCT(BlueprintType)
struct FBHZBTONGSIGNUPRANKDATA {
	GENERATED_USTRUCT_BODY()
		/// 帮会DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongDBID = "";
	/// 帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName = "";
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongLevel = 0;
	/// 活跃度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Activity = "";
	/// 帮会人数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongMemNum = 0;
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Camp = 0;
};

USTRUCT(BlueprintType)
struct FBHZBPOINTDATA {
	GENERATED_USTRUCT_BODY()
		/// 据点编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Index = 0;
	///据点类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 PointType;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 declareWarState = 1;
	/// 占领据点玩家DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString OccupyPlayerDBID = "";
	/// 占领据点帮会DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString OccupyTongDBID = "";
	/// 据点战斗结束时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString FightEndTime = "";
	/// 重置结束的时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString RestEndTime = "";
	/// 准备结束的时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ReadyEndTime = "";
	/// 占领帮会名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString OccupyTongName = "";
	/// 进攻队伍编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 AttackGroupTeamID = 0;
	/// 防守队伍编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 JoinProtectGroupTeamID = 0;
	/// 进攻方帮会DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DeclareTongDBID = "";
};

USTRUCT(BlueprintType)
struct FBHZBMAPHOMEBARRACKSDATA {
	GENERATED_USTRUCT_BODY()
	/// 大本营编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 Index = -1;
	/// 大本营位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector Position;
	/// 大本营DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString BelongTongDBID = "";
	/// 大本营名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString Name = "";
};
USTRUCT(BlueprintType)
struct FBHZBMEMBERPOSDATA {
	GENERATED_USTRUCT_BODY()
	/// 成员分组
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 GroupID = 0;
	/// 成员位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FVector Position;
};
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBHZB_POINT_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	/// 据点编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Index")
	int32 Index = 0;
	/// 据点名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PointName")
	FString PointName;
	/// 据点类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PointType")
	NPCEXTPOINT_TYPE PointType = NPCEXTPOINT_TYPE::NPCEXTPOINT_TYPE_LOWER_LEVEL;
	/// 据点进入PVEspace
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PVESpaceScriptID")
	FString PVESpaceScriptID;
	/// 据点进入PVPspace
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PVPSpaceScriptID")
	FString PVPSpaceScriptID;
	/// 据点位置信息
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PointPosition")
	FVector PointPosition;
	/// 据点准备时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ReadyTime")
	float ReadyTime = 0;
	/// 据点加入最大人数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MaxJoinPlayerNum")
	int32 MaxJoinPlayerNum = 0;
	/// 据点休整时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "RestTime")
	float RestTime = 0;
};
USTRUCT(BlueprintType)
struct FBHZBTONGTEAMDATA {
	GENERATED_USTRUCT_BODY()
	/// 帮会队伍编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	int32 TeamNumber = 0;
	/// 据点编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PointNumber = 0;
	/// 据点状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PointState = 0;
	/// 据点名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PointName = "";
};
USTRUCT(BlueprintType)
struct FBHZBTONGOCCUPYPOINTDATA {
	GENERATED_USTRUCT_BODY()
		/// 据点编号
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PointNumber = 0;
	/// 据点状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PointState = 0;
	/// 据点名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PointName = "";
	bool operator ==(const FBHZBTONGOCCUPYPOINTDATA& other)
	{
		if (other.PointNumber == PointNumber)
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
struct FBHZBTONGWARMSGDATA {
	GENERATED_USTRUCT_BODY()
		/// 消息ID
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 StatusID = 0;
	/// 消息内容
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StatusArgs = "";
};

USTRUCT(BlueprintType)
struct FBHZBTONGWARDETAIL {
	GENERATED_USTRUCT_BODY()
	/// 帮会DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FString TongDBID = "";
	/// 帮会积分
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Integral = 0;
	/// 帮会排名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Rank = 0;
	/// 帮会占领据点数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 OccupyPointAmount = 0;
	/// 帮会组队数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, FBHZBTONGTEAMDATA> TeamDatas;
	/// 帮会占领据点数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FBHZBTONGOCCUPYPOINTDATA> OccupyPointDatas;
	/// 帮会战场消息数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FBHZBTONGWARMSGDATA> warMsgDatas;
};

UENUM(BlueprintType)
enum class POINTREQURY_TYPE : uint8
{
	///没有请求
	POINTREQURY_TYPE_NONE = 0	    UMETA(DisplayName = "POINTREQURY_TYPE_NONE"),
	///请求详情界面
	POINTREQURY_TYPE_RMOUSE_MENUE = 1   UMETA(DisplayName = "POINTREQURY_TYPE_RMOUSE_MENUE"),
	///右键点击请求
	REQURYPOINT_TYPE_RMOUSE_CLICK = 2   UMETA(DisplayName = "REQURYPOINT_TYPE_RMOUSE_CLICK"),
	///无操作请求
	REQURYPOINT_TYPE_NO_OPERATE = 3     UMETA(DisplayName = "REQURYPOINT_TYPE_NO_OPERATE"),
};

USTRUCT(BlueprintType)
struct FALLBHZBTONGINTEGRALDATA {
	GENERATED_USTRUCT_BODY()
		/// 帮会DBID
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongDBID = "";
	/// 帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName = "";
	/// 帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TongLevel = 0;
	/// 总积分
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TotalIntegral = 0;
	/// 帮会积分
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Integral = 0;
	/// 阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Camp = 0;
	/// 时间场次
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StartTime = "";
};


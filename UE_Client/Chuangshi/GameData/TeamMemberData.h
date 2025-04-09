#pragma once
#include "CoreMinimal.h"
#include "TeamMemberData.generated.h"
/**
* 文件名称：TeamMemberData.h
* 功能说明：一个队伍成员的数据
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-03-15
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTeamMemberData
{
	GENERATED_USTRUCT_BODY()
		FTeamMemberData() {};
public:
	// DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PlayerDBID")
		FString PlayerDBID;

	// 玩家ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EntityID")
		int32 EntityID = 0;

	// 玩家名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PlayerName")
		FString PlayerName;

	// 玩家职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Profession")
		int32 Profession = 0;

	// 玩家阵营
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Camp")
		int32 Camp = 0;

	// 玩家等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Level")
		int32 Level = 0;

	// 玩家性别
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Gender")
		int32 Gender = 0;

	// 在线状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "OnLineState")
		int32 OnLineState = 0;

	// 玩家血量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HP")
		int32 HP = 0;

	// 玩家最大血量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "HPMax")
		int32 HPMax = 0;

	// 玩家法力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MP")
		int32 MP = 0;

	// 玩家最大法力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MPMax")
		int32 MPMax = 0;

	// 玩家地图ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SpaceScriptID")
		FString SpaceScriptID;

	// 玩家大地图分线Number 其他地图为0
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "LineNumber")
		int32 LineNumber = 0;
public:
	bool operator==(const FTeamMemberData &Tm1)const{
		return (Tm1.EntityID == EntityID);
	}
	
};
#pragma once

#include "UObject/NoExportTypes.h"
#include "GameData/TongData.h"
#include "GameData/GameDefine.h"
#include "Util/EventDelegate.h"
#include "Misc/Variant.h"
#include "TongClass.generated.h"

/**
* 文件名称：TongClass.h
* 功能说明：帮会实例
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-01-26
*/

class UJsonFieldData;

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UTongMember : public UObject
{
	GENERATED_BODY()


public:
	UPROPERTY(BlueprintReadOnly)
		FString name;
	UPROPERTY(BlueprintReadOnly)
		FString DBID;
	UPROPERTY(BlueprintReadOnly)
		int32 id = 0;
	UPROPERTY(BlueprintReadOnly)
		int32 level = 0;
	UPROPERTY(BlueprintReadOnly)
		int32 profession = 0;
	UPROPERTY(BlueprintReadOnly)
		int32 title = 0;
	UPROPERTY(BlueprintReadOnly)
		int32 exp = 0;
	///本周帮贡
	UPROPERTY(BlueprintReadOnly)
		int32 weekContribution = 0;
	///剩余帮贡
	UPROPERTY(BlueprintReadOnly)
		int32 contribution = 0;
	///总帮贡
	UPROPERTY(BlueprintReadOnly)
		int32 totalContribution = 0;
	///所在地
	UPROPERTY(BlueprintReadOnly)
		FString localSpace;
	///登录时间(用于客户端的显示)
	UPROPERTY(BlueprintReadOnly)
		FString offLineTime;
	///登录时间
	UPROPERTY(BlueprintReadOnly)
		FString offTime;
	///是否被禁言
	UPROPERTY(BlueprintReadOnly)
		int32 isGag = 0;
	///玩家总兵力
	UPROPERTY(BlueprintReadOnly)
		int32 SoldierAmount = 0;
	///玩家军衔
	UPROPERTY(BlueprintReadOnly)
		int32 MilitaryRank = 0;
	///屏蔽列表[DBID]
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> Blocklist;
};

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UTongObject : public UObject
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable)
		UTongMember* GetMemberByDBID(const FString PlayerDBID);

	UFUNCTION(BlueprintCallable)
		TArray<UTongMember*> GetMembersBySoldierData(const TArray<FString> removeMemberDIBDs,const int32& soldierAmount,const int32& militaryRank);

	void initTongData(const FVariant& JsonData);
	void initMemberData(const FVariant& JsonData, FTraceCallback TraceCallback);
	void OnKickTongMember(const FString& kickerDBID, const FString& beKickerDBID);
	void SortMember();
	void calculOffTimeStr(UTongMember* member);

	UFUNCTION(BlueprintCallable)
		bool isTongMoneyLow();				//帮会资金是否低于帮会最低维护资金
	UFUNCTION(BlueprintCallable)
		int32 getDayExtraDeductActivity(); //每日结算时会额外扣除点活跃度

public:
	UPROPERTY(BlueprintReadOnly)
		FString TongDBID;
	UPROPERTY(BlueprintReadOnly)
		FString TongName;
	UPROPERTY(BlueprintReadOnly)
		int32 TongLevel = 0;
	UPROPERTY(BlueprintReadOnly)
		int64 TongMoney = 0;
	///帮主DBID
	UPROPERTY(BlueprintReadOnly)
		FString TongLeaderDBID;
	///帮会权限
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> TongGrades;
	///帮会职称
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> TongTitleNames;
	///帮会公告
	UPROPERTY(BlueprintReadOnly)
		FString TongAffiche;
	///帮会招募公告
	UPROPERTY(BlueprintReadOnly)
		FString TongRecruitAffiche;
	///帮会活跃度
	UPROPERTY(BlueprintReadOnly)
		int32 TongActivity = 0;
	///升级需要的帮会活跃度
	UPROPERTY(BlueprintReadOnly)
		int32 TongUpGradeActivity = 0;
	///帮会最小活跃度
	UPROPERTY(BlueprintReadOnly)
		int32 MinActivity = 0;
	///帮会成长度
	UPROPERTY(BlueprintReadOnly)
		int32 TongGrowth = 0;
	///累计签到次数
	UPROPERTY(BlueprintReadOnly)
		int32 SignTime = 0;
	///捐献金钱
	UPROPERTY(BlueprintReadOnly)
		int64 DonateMoney = 0;
	///帮会成员
	UPROPERTY(BlueprintReadOnly)
		TMap<FString, UTongMember*> TongMembers;
	///帮会人数
	UPROPERTY(BlueprintReadOnly)
		int32 TongNum = 0;
	///帮会最大人数
	UPROPERTY(BlueprintReadOnly)
		int32 TongMaxNum = 0;
	///帮会建筑
	UPROPERTY(BlueprintReadOnly)
		TMap<TONG_BUILD_TYPE,int32> TongBuildLevel;
	///帮会正在研发的技能
	UPROPERTY(BlueprintReadOnly)
		FResearchSkillDATA CurResearSkill;
	///帮会暂停研发的技能
	UPROPERTY(BlueprintReadOnly)
		TArray<FResearchSkillDATA> PauseSkill;
	///已经研发的技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> HasResearSkillList;
	///当前已研发的最高等级技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> CurSkillLevelList;
	///帮会联盟
	UPROPERTY(BlueprintReadOnly)
		FString TongLeague;
	///占领城市
	UPROPERTY(BlueprintReadOnly)
		FString TongCity;
	///帮会神兽
	UPROPERTY(BlueprintReadOnly)
		int32 ShenShou = 0;
	///是否已经签到
	UPROPERTY(BlueprintReadOnly)
		bool isSign;
	///是否已经领取俸禄
	UPROPERTY(BlueprintReadOnly)
		bool isGetSalary;
	///玩家自己的帮会信息
	UPROPERTY(BlueprintReadOnly)
		UTongMember* PlayerMember;
	///帮会争霸分配方式
	UPROPERTY(BlueprintReadOnly)
		TONG_PICKUP_TYPE allocation;
	///帮会掠夺分配方式
	UPROPERTY(BlueprintReadOnly)
		TONG_PICKUP_TYPE BHLDAllocation;
};

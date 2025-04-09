#pragma once

#include "GameData/GameDefine.h"
#include "CsvTableRowBase.h"
#include "TongData.generated.h"

/**
* 文件名称：TongData.h
* 功能说明：帮会数据
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-1-13
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongMemberGrade
{
	GENERATED_USTRUCT_BODY()

	///帮会职称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_TITLE_TYPE TongType;
	///系统锁定权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SystemGrade")
		TArray<TONG_GRADE_TYPE> TONG_SYSTEM_GRADE;
	///可操作权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DefaultGrade")
		TArray<TONG_GRADE_TYPE> TONG_DEFAULT_GRADE;
	///禁止权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ForbidGrade")
		TArray<TONG_GRADE_TYPE> TONG_FORBID_GRADE;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongGradeDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///帮会职称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "帮会职务")
		TONG_TITLE_TYPE TongType;
	///帮会界面对应职务
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "帮会界面对应职务")
		TONG_TITLE_TYPE uiTongType;
	///系统锁定权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SystemGrade")
		TArray<TONG_GRADE_TYPE> TONG_SYSTEM_GRADE;
	///可操作权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DefaultGrade")
		TArray<TONG_GRADE_TYPE> TONG_DEFAULT_GRADE;
	///禁止权限
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ForbidGrade")
		TArray<TONG_GRADE_TYPE> TONG_FORBID_GRADE;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongSkillDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SkillID")
		int32 SkillID = 0;
	///技能类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SkillType")
		TONG_SKILL_TYPE SkillType;
	// 技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Level")
		int32 Level = 0;
	// 下一等级技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "NextSkill")
		int32 NextSkill = 0;
	//研发需要帮会资金
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ResearchReqTongMoney")
		int32 ResearchReqTongMoney = 0;
	//研发需要做多少帮会日常
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ResearchReqDaily")
		int32 ResearchReqDaily = 0;
	//研发需要研究院等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ResearchReqBuildIngLevel")
		int32 ResearchReqBuildIngLevel = 0;
	//学习需要帮会职务
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StudyReqTitle")
		int32 StudyReqTitle = 0;
	//学习需要金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StudyReqMoney")
		int32 StudyReqMoney = 0;
	//学习需要帮贡
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StudyReqContribution")
		int32 StudyReqContribution = 0;
	//学习需要修为
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "StudyReqXiuweiLevel")
		int32 StudyReqXiuweiLevel = 0;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongUpGradeData
{
	GENERATED_BODY()
	///升级消耗金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 upGradeMoney = 0;
	///升级消耗成长度
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 upGradeGrow = 0;
	/// 需要帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 needTongLevel = 0;
	///升级效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString effect;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongBuildLevelDATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

	/// 建筑等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level = 0;
	///升级消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<TONG_BUILD_TYPE, FTongUpGradeData> upGradeData;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongJoinData
{
	GENERATED_BODY()
	//帮会DBID
	UPROPERTY(BlueprintReadOnly)
		FString TongDBID;
	//帮会名称
	UPROPERTY(BlueprintReadOnly)
		FString TongName;
	// 帮会等级
	UPROPERTY(BlueprintReadOnly)
		int32 TongLevel = 0;
	// 活跃度
	UPROPERTY(BlueprintReadOnly)
		int32 TongActivity = 0;
	// 帮会人数
	UPROPERTY(BlueprintReadOnly)
		int32 TongNum = 0;
	// 帮会总人数
	UPROPERTY(BlueprintReadOnly)
		int32 TotalNum = 0;
	// 帮主名称
	UPROPERTY(BlueprintReadOnly)
		FString LeaderName;
	// 帮会资金
	UPROPERTY(BlueprintReadOnly)
		int64 Money;
	//帮会招募公告
	UPROPERTY(BlueprintReadOnly)
		FString RecruitAffiche;
	//帮会联盟
	UPROPERTY(BlueprintReadOnly)
		FString TongLeague;
	//占领城市
	UPROPERTY(BlueprintReadOnly)
		FString OccupyCity;
	//神兽
	UPROPERTY(BlueprintReadOnly)
		int32 Shenshou = 0;
	//帮主称号
	UPROPERTY(BlueprintReadOnly)
		FString PersonTitle;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPlayerJoinData
{
	GENERATED_BODY()
	//玩家名字
	UPROPERTY(BlueprintReadOnly)
		FString name;
	//DBID
	UPROPERTY(BlueprintReadOnly)
		FString DBID;
	//等级
	UPROPERTY(BlueprintReadOnly)
		int32 level = 0;
	//门派
	UPROPERTY(BlueprintReadOnly)
		int32 profession = 0;

	FORCEINLINE bool operator==(const FPlayerJoinData& other) const
	{
		if (this->DBID.Equals( other.DBID))
		{
			return true;
		}
		return false;
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FResearchSkillDATA
{
	GENERATED_BODY()
	// 技能ID
	UPROPERTY(BlueprintReadOnly)
		int32 SkillID = 0;
	// 研发技能进度
	UPROPERTY(BlueprintReadOnly)
		int32 Progress = 0;

	FORCEINLINE bool operator==(const FResearchSkillDATA& other) const
	{
		if (this->SkillID == other.SkillID)
		{
			return true;
		}
		return false;
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongEventDATA
{
	GENERATED_BODY()
	// 时间
	UPROPERTY(BlueprintReadOnly)
		FDateTime Time;
	// 事件类型
	UPROPERTY(BlueprintReadOnly)
		int32 EventType = 0;
	//类事件类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_EVENT_SET_TYPE ClassEventType;
	// 事件提示
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> EventStr;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongEventMapping : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
	//事件类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_EVENT_TYPE EventType;
	//类事件类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_EVENT_SET_TYPE ClassEventType;
	//事件消息
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> EventStr;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongStoreEventMapping : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
	//帮会仓库事件类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_STORE_EVENT_TYPE EventType;
	//帮会仓库事件消息
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FString> EventStr;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongStoreEventData
{
	GENERATED_BODY()
	// 时间
	UPROPERTY(BlueprintReadOnly)
		FDateTime Time;
	// 事件类型
	UPROPERTY(BlueprintReadOnly)
		int32 EventType = 0;
	// 事件提示
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> EventStr;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongSalaryData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
	///<职称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TONG_TITLE_TYPE TitleType;
	///<奖励物品ID列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> ItemIDList;
	///<奖励物品数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> ItemCount;
};

//帮会邀请数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FTongInviteData
{
	GENERATED_USTRUCT_BODY()
public:
	///<邀请人名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString InviterName;
	///<邀请人EntityID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 InviterEntityID;
	///<帮会名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongName;
	///<邀请人DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TongDBID;

	FORCEINLINE bool operator==(const FTongInviteData& Other) const
	{
		if (this->InviterEntityID == Other.InviterEntityID && this->TongDBID == Other.TongDBID)
		{
			return true;
		}
		else
		{
			return false;
		}
	}
};

//帮会争霸界面候选人数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBHZBCandidate
{
	GENERATED_USTRUCT_BODY();
public:
	///候选人DBID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString CandidateDBID;
	///候选人名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString CandidateName;
	///候选人兵力
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SoldierAmount = 0;
        ///队伍编号
        UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 TeamGroupID = 0;
	///是否为队长
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
                bool IsCaptain = false;
	FORCEINLINE bool operator==(const FBHZBCandidate& Other) const
	{
		if (this->CandidateDBID == Other.CandidateDBID)
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
struct CHUANGSHI_API FTongLevelData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///帮会等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 level;
	///帮会升级需要消耗活跃度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "useActivity")
		int32 useActivity;
	///帮会升级需要消耗资金
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "useMoney")
		int32 useMoney;
	///每天消耗活跃度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "perActivity")
		int32 perActivity;
	///活跃度最小值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "minActivity")
		int32 minActivity;
	///帮会掠夺战锁定帮会资金
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "lockMoney")
		int32 lockMoney;
	///帮会最低维护资金
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "lowMoney")
		int32 lowMoney;
	///帮会资金过低扣除活跃度比例（百分比）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "perActivityForLowMoney")
		int32 perActivityForLowMoney;
};
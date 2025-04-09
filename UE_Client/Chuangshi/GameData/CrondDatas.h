#pragma once

#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "CrondDatas.generated.h"

/**
* 文件名称：CrondDatas.h
* 功能说明：日程管理器数据
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2017:4:14
*/


//---------------------------------------------分割线（上面的数据结构准备清理（QRN））-------------------------------------------------------------------
UENUM(BlueprintType)
enum class ACTIVE_TYPE : uint8
{
	//休闲玩法
	ACTIVE_TYPE_ARDER	= 0,
	//PVP
	ACTIVE_TYPE_PVP		= 1,
	//PVE
	ACTIVE_TYPE_PVE		= 2,
};

UENUM(BlueprintType)
enum class ACTIVE_STATUS : uint8
{
	//正在进行
	ACTIVE_STATUS_ACTIVATING= 0,
	//已结束
	ACTIVE_STATUS_END		= 1,
	//未开始
	ACTIVE_STATUS_NOT_START = 2,
	//全天
	ACTIVE_STATUS_ALL_DAY	= 3,
};

UENUM(BlueprintType)
enum class ACTIVE_REWARD_TYPE : uint8
{
	ACTIVE_REWARD_TYPE_MONEY				= 0, //金币奖励
	ACTIVE_REWARD_TYPE_EXP					= 1, //经验奖励
	ACTIVE_REWARD_TYPE_XIUWEI				= 2, //修为奖励
	ACTIVE_REWARD_TYPE_POTENTIAL			= 3, //潜能奖励
	ACTIVE_REWARD_TYPE_EXP_TONG_CONTRIBUTE	= 4, //帮贡奖励
	ACTIVE_REWARD_TYPE_EXP_TONG_MONEY		= 5, //帮会资金奖励
	ACTIVE_REWARD_TYPE_FEATS				= 6, //功勋奖励
	ACTIVE_REWARD_TYPE_MORALE				= 7, //战意奖励
	ACTIVE_REWARD_TYPE_ITEM					= 8, //物品奖励
};

//提醒类型
UENUM(BlueprintType)
enum class CROND_REMIND_TYPE : uint8
{
	// 不提醒
	No_Remind = 0,
	// 开启时
	Is_Opening = 1,
	// 提前5分钟
	Before_FiveMinutes = 2,
	// 提前10分钟
	Before_TenMinutes = 3,
	// 提前半小时
	Before_HalfAnHour = 4,
};

UENUM(BlueprintType)
enum class CROND_TYPE : uint8
{
	///普通活动日程
	CROND_TYPE_COMMON = 0,
	///帮会活动日程
	CROND_TYPE_TONG = 1,
};

///周历配置数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FWeekCrondConfigData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FWeekCrondConfigData() {}
	///周几（0-6对应周一到周日）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "WeekDay")
		int32 wday;
	///每周几的活动总结
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ActivitySummary")
		FString ActivitySummary;
	///每周几的特色玩法总结
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SpecialPlaySummary")
		FString SpecialPlaySummary;
};

///活动配置数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FNewCrondConfigData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FNewCrondConfigData() {}
public:
	///配置数据ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "scriptID")
		FString scriptID;
	///活动名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "crondName")
		FString crondName;
	///活动类型 休闲玩法、PVP、PVE等,活动不能同时有多种类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "actType")
		ACTIVE_TYPE actType;
	///玩法类型 日程玩法和特色玩法，活动可同时具体多种类型，A|B
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "playType")
		FString playType;
	///活动推荐星级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "star")
		int32 star = 0;
	///活动评级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "actGrade")
		int32 actGrade = 0;
	///活动图片编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "pictureNumber")
		FString pictureNumber;
	///奖励类型 金钱、经验等，用于玩法推荐
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "rewardType")
		FString rewardType;
	///推荐人数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "referrals")
		int32 referrals = 0;
	///活动描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "description")
		FString description;
	///参与方式描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "partInDes")
		FString partInDes;
	///奖励列表
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "reward")
		FString reward = "";
	///额外奖励
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "extraReward")
		FString extraReward = "";
	///活动奖励金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "money")
		int64 money = 0;
	///需要等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "level")
		int32 level = 0;
	///活动总次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "amount")
		int32 amount = 0;
	///活动地点（点击前往导航到的位置）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "place")
		FString place;
	///活动时间段
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "timeSlot")
		FString timeSlot;
	///玩法推荐描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "recommend")
		FString recommend = "";
	///类型（对应服务器csdefine中的ACTIVITY_TYPE_LIST）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "type")
		int32 type = 0;//不会加载其他资源得浅检查
	///日程类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "crondType")
		CROND_TYPE crondType;
public:
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		TArray<FString> RewardTypes;
		rewardType.ParseIntoArray(RewardTypes, TEXT("|"), true);
		for (auto RType : RewardTypes)
		{
			if (RType != "0")
			{
				ACTIVE_REWARD_TYPE _type = (ACTIVE_REWARD_TYPE)FSTRING_TO_INT(RType);
				int IntType = FSTRING_TO_INT(RType);
				if (IntType == 0 || IntType < 0 || IntType > (int)ACTIVE_REWARD_TYPE::ACTIVE_REWARD_TYPE_ITEM)
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"rewardType\" config error"));
				}
			}
			
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

//活动提醒设置数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCrondRemindSettingData
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "scriptID")
		FString scriptID;
	///活动名称
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "name")
		FString name;
	///活动时间
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "time")
		FString time;
	///提醒类型
	///	0：不提醒
	///	1：开启时
	///	2：提前5分钟
	///	3：提前10分钟
	///	4：提前半小时
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "remindType")
		CROND_REMIND_TYPE remindType = CROND_REMIND_TYPE::Before_FiveMinutes;

	FORCEINLINE bool operator==(const FCrondRemindSettingData& other) const
	{
		if (this->scriptID.Equals(other.scriptID))
		{
			return true;
		}
		return false;
	}
};

///活动状态
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCrondActivityStatus
{
	GENERATED_BODY()

	//开始时间
	int32 startTime = 0;
	//状态描述（正在进行、具体开始时间……）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "statusInfo")
		FString statusInfo = "";
	///状态
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "status")
		ACTIVE_STATUS status = ACTIVE_STATUS::ACTIVE_STATUS_END;
};

//每天活动数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCrondData
{
	GENERATED_BODY()
	///活动ID
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "scriptID")
		FString scriptID = "";
	///活动日期
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "date")
		FString date;
	///周几活动(0-6对应周一到周日)
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "wday")
		int32 wday;
	///活动配置
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "crondConfig")
		FNewCrondConfigData crondConfig;
	///活动时间段
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "status")
		TArray<FCrondActivityStatus> status;
	//当前的状态
	//（用来进行活动排序，当前活动一天内有多个活动时间段，其中一个开启了的话，也应该显示在前）
	FCrondActivityStatus curStatus;
};

//每天活动数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FDayCrondData
{
	GENERATED_BODY()

	///活动日期
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "date")
		FString date;
	///周几活动(0-6对应周一到周日)
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "wday")
		int32 wday;
	///活动数据
	UPROPERTY(EditAnywhere, BlueprintReadOnly, DisplayName = "crondDatas")
		TMap<FString, FCrondData> crondDatas;
};

//活动图片配置表
USTRUCT(BlueprintType)
struct CHUANGSHI_API FCrondTexturePath : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//活动图片编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString pictureNumber;
	//编号对应贴图路径(活动列表介绍活动贴图)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> TexturePath1;
	//编号对应贴图路径(周历玩法推荐活动贴图)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> TexturePath2;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;

		if (TexturePath1.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(TexturePath1.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath1\" resource does not exist"));
				bHasError = true;
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath1\" is None"));
			bHasError = true;
		}
		if (TexturePath2.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(TexturePath2.ToString()))
			{
				ResultInfo.Result = Error;
				if (bHasError)
				{
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"TexturePath2\" resource does not exist"));
				}
				else
				{
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath2\" resource does not exist"));
				}
			}
		}
		else
		{
			ResultInfo.Result = Error;
			if (bHasError)
			{
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"TexturePath2\" is None"));
			}
			else
			{
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath2\" is None"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
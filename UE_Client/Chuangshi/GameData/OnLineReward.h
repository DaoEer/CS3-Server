// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "OnLineReward.generated.h"

/**
* 文件名称：OnLineReward.h
* 功能说明：在线奖励数据
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2018-8-16
*/

///@struct FAREA_DATA
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSignInData
{
	GENERATED_USTRUCT_BODY()

public:
	///签到年份
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Year")
		int32 Year;
	///签到月份
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Month")
		int32 Month;
	///签到日期
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Days")
		TArray<int32> Days;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSignInReward
{
	GENERATED_USTRUCT_BODY()

public:
	///奖品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 GiftID;
	///数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Amount;
	///绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BindType;
};

/// 签到奖励
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSignInRewardData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	///物品
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Gift;
	///绑定
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BindType;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		if (this->Gift.IsEmpty())
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Gift: value is empty!\n"));
			return;
		}
		else
		{
			for (auto gifts : UGolbalBPFunctionLibrary::SplitString(this->Gift, false, TEXT(";")))
			{
				for (auto gift : UGolbalBPFunctionLibrary::SplitString(gifts, false, TEXT(":")))
				{
					if (gift != "0" && FSTRING_TO_INT(gift) == 0)
					{
						ResultInfo.Result = Error;
						ResultInfo.CheckLog = FString::Printf(TEXT("Gift: \"%s\" is config error!\n"), *this->Gift);
						return;
					}
				}
			}
		}
		ResultInfo.Result = Ok;
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};

UENUM(BlueprintType)
enum class SIGN_IN_REWARD_TYPE : uint8
{
	///不可领取（签到奖励）
	REWARD_NONE        UMETA(DisplayName = "REWARD_NONE"),
	///可领取（签到奖励）
	REWARD_ACTIVE        UMETA(DisplayName = "REWARD_ACTIVE"),
	///已经领取（签到奖励）
	REWARD_RECEIVER        UMETA(DisplayName = "REWARD_RECEIVER"),
};


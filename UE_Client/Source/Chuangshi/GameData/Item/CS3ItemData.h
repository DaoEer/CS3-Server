// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "CS3ItemData.generated.h"

/**
* 文件名称：CS3ItemData.h
* 功能说明：物品数据配置表
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-12
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCS3ItemData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ItemID = 0;
	///物品名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ItemName;
	///脚本名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Script;
	///图标ID（@DT_ItemIconCfg）
	///注意：
	///	不是图标的资源名称，而是要在DT_ItemIconCfg中注册使用
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Icon;
	///物品的大分类
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Type = 0;
	///绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BindType = 0;
	///拾取类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PickUpType = 0;
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level = 0;
	//品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Quality = 0;
	///价格
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Price = 0;
	///累加类型（@CST-4375）
	///	0：不可叠加；格式：0
	///	1：可叠加；格式：1|堆叠上限（不得缺省）
	///	2：可计次；格式：2|次数上限（不得缺省,-1为无限次数）|是否显示剩余次数（缺省0＝不显示；1＝显示）
	///	3：可充能；格式：3|充能点数上限（不得缺省）|当前充能点数（不得缺省）|是否显示当前充能点数（缺省0＝不显示；1＝显示）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString StackAmount;
	///最大携带数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 MaxTakeAmount = 0;
	///能否出售
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CanSell = 0;
	///能否主动销毁
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CanDestroy = 0;
	///物品描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Describe;
	///性别要求
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReqGender = 0;
	///职业限制
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ReqClasses;
	///使用等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReqLevel = 0;
	///使用j境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReqJingJieLevel = 0;
	///使用地图
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ReqSpace;
	///技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SkillID = 0;
	///是否退货
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CanReturn = 0;
	///使用限量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString UseAmount;
	///持有效果ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString HoldEffectID;
	///物品限时
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString LimitTime;
	///Param1
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param1;
	///Param2
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param2;
	///Param3
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param3;
	///Param4
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param4;
	///Param5
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Param5;
	///(纯客户端字段)物品是否不能收购，默认为0可收购，1为不可收购
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CannotCollect = 0;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		bool bHasError = false;
		TArray<FString> StackAmountData = SplitString(StackAmount, false, TEXT("|"));
		if (StackAmountData.Num() > 0)
		{
			int IntTemp0 = FCString::Atoi(*StackAmountData[0]);
			if (StackAmountData[0].TrimStartAndEnd() != "0" && IntTemp0 == 0)
			{
				bHasError = true;
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
			}
			else if (IntTemp0 != 0)
			{
				if (StackAmountData.Num() >= 2)
				{
					int IntTemp1 = FCString::Atoi(*StackAmountData[1]);
					if (StackAmountData[1].TrimStartAndEnd() != "0" && IntTemp1 == 0)
					{
						bHasError = true;
						ResultInfo.Result = Error;
						ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
					}

				}
				else
				{
					bHasError = true;
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"StackAmount\" config error"));
				}
			}
		}
		TArray<FString> ClassesData = SplitString(ReqClasses, false, TEXT("|"));
		if (ClassesData.Num() > 0)
		{
			for (auto Data : ClassesData)
			{
				if (Data.TrimStartAndEnd() != TEXT("") && FCString::Atoi(*Data) == 0)
				{
					ResultInfo.Result = Error;
					if (bHasError)
					{
						ResultInfo.CheckLog += FString::Printf(TEXT("; \"ReqClasses\" config error"));
					}
					else
					{
						ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ReqClasses\" config error"));
					}
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

/// 装备附加属性区间
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEquipPropertyInterval : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 LevelSection = 0;
	///职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Class = 0;
	///部位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ModelPart = 0;
	///属性编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 PropertyID = 0;
	///区间上限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Min = 0;
	///区间下限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Max = 0;
	///强化附加属性区间下限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IntensifyMin = 0;
	///强化附加属性区间上限
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 IntensifyMax = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FEquipShuffleData
{
	GENERATED_USTRUCT_BODY()
		FEquipShuffleData() {};
public:
	///属性ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PropertyID")
		int32 PropertyID = 0;
	///属性值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PropertyValue")
		int32 PropertyValue = 0;
	///属性最大值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MaxPropertyValue")
		int32 Max = 0;
};
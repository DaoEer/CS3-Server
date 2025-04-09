// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BarracksTableData.generated.h"

/**
* 文件名称：BarracksTableData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-23
*/

///解锁条件类型
UENUM(BlueprintType)
enum class ENUM_UNLOCK_CONDITION_TYPE : uint8
{
	///	是否有占领练兵场
	///参数1:占领练兵场类型；可不填 (1代表低级 2 代表中级 3代表高级)
	///参数2:目标等级
	///参数3:无
	UnLockConditionOccupyTrain = 0  UMETA(DisplayName = "UnLockConditionOccupyTrain"),
};

UENUM(BlueprintType)
enum class ENUM_BARRACKS_SOLDIER_TYPE : uint8
{
	///兵种
	BARRACKS_SOLDIER_COMMON_TYPE = 0  UMETA(DisplayName = "BARRACKS_SOLDIER_COMMON_TYPE"),
	///亲卫
	BARRACKS_SOLDIER_GUARD_TYPE = 1  UMETA(DisplayName = "BARRACKS_SOLDIER_GUARD_TYPE"),
};

///解锁条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_UNLOCKS_CONDITION
{
	GENERATED_BODY()
	///条件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ConditionType")
	ENUM_UNLOCK_CONDITION_TYPE ConditionType;
	///参数1（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Param1")
		FString Param1;
	///参数2（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Param2")
		FString Param2;
	///参数3（字符串）
	///支持：
	///	功能由具体类型定义（详见具体类型相关说明）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Param3")
		FString Param3;
};

///解锁条件
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_UNLOCKS_LEVEL_CONDITION
{
	GENERATED_BODY()
	/// 目标等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "TargetLevel")
	int32 TargetLevel = 0;
	///条件类型
	///	不同类型，决定着不同的参数定义
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Conditions")
	TArray<FBARRACKS_UNLOCKS_CONDITION> Conditions;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBARRACKS_TABLE_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	///兵名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite,  DisplayName = "SoldierName")
	FString SoldierName;
	///兵ScriptID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ScriptID")
	FString ScriptID;
	///兵图标路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite,  DisplayName = "Icon")
	TSoftObjectPtr<UTexture2D> Icon;
	///拥有最大数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MaxHaveAmount")
	int32 MaxHaveAmount = 0;
	///部队拥有的最大数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ArmyMaxAmount")
	int32 ArmyMaxAmount = 0;
	///兵的类型 (兵种、亲卫)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "SoldierType")
	ENUM_BARRACKS_SOLDIER_TYPE SoldierType;
	///兵的最大等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MaxUpLevel")
	int32 MaxUpLevel = 0;
	///招募兵消耗的金钱
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CostMoney")
	int32 CostMoney = 0;
	///兵的普通技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CommonSkillIDs")
	TArray<int32> CommonSkillIDs;
	///指挥技能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CommandSkillID")
	int32 CommandSkillID;
	///解锁兵的条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "UnLockConditions")
	TArray<FBARRACKS_UNLOCKS_CONDITION> UnLockConditions;
	///解锁兵等级的条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "UnLockLevelConditions")
	TArray<FBARRACKS_UNLOCKS_LEVEL_CONDITION> UnLockLevelConditions;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (Icon.ToSoftObjectPath().IsValid())
		{
			if (!CheckResourceFileIsExist(Icon.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"Icon\" resource does not exist"));
			}
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "LbcData.generated.h"


/**
* 文件名称：LbcData.h
* 功能说明：练兵场配置表 JIRA CST-12015
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-8-19
*/

const uint8 LBC_MAX_LINE = 10;

USTRUCT(BlueprintType)
struct CHUANGSHI_API FLbcDatas : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///练兵场序号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 index;
	///练兵场等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 level;
	///练兵场名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lbcName;
	///NPC位置 用于显示大地图城镇图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector position;

};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FRoleLbcData
{
	GENERATED_USTRUCT_BODY()
		FRoleLbcData() {};
		FRoleLbcData(int32 index, uint8 level, uint8 line, uint8 status, FString lbcName, FVector position):
					index(index), level(level), line(line), status(status), lbcName(lbcName), position(position){};
		///练兵场序号
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 index;
	///练兵场等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 level;
	///练兵场分线
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 line;
	///练兵场状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 status;
	///练兵场名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lbcName;
	///NPC位置 用于显示大地图城镇图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector position;
};

/**
* 练兵场状态
*/
UENUM(BlueprintType)
enum class LBC_STATUS : uint8
{
	/// 未占领
	LBC_STATUS_NORMAL = 1 UMETA(DisplayName = "LBC_STATUS_NORMAL"),
	/// 被宣战
	LBC_STATUS_DELCARED = 2 UMETA(DisplayName = "LBC_STATUS_DELCARED"),
	/// 争夺中
	LBC_STATUS_FIGHT = 3 UMETA(DisplayName = "LBC_STATUS_FIGHT"),
	///已占领
	LBC_STATUS_OCCUPIED = 4 UMETA(DisplayName = "LBC_STATUS_OCCUPIED"),
	
};


//练兵场状态信息
struct FLBC_STATUS
{
public:
	uint32 index;
	uint8 line;
	uint8 status;

	FLBC_STATUS(FVariant variant);
};


//练兵场宣战信息
USTRUCT(BlueprintType)
struct  FLBC_DECLARE_INFO
{
	GENERATED_USTRUCT_BODY()
		FLBC_DECLARE_INFO() {};
public:
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 level;
	///分线
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 line;
	///练兵场名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lbcName;
	///状态
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 status;
	///占领者名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString occupierName;
	///占领者职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 occupierProfession;
	///宣战者名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString declarerName;
	///宣战者职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 declarerProfession;
	///Index
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 index;
	///争夺时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int64 attackTime;
	///开战倒计时
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 countDown;

	FLBC_DECLARE_INFO(const FVariant& variant);
};

//练兵场占领信息
USTRUCT(BlueprintType)
struct  FLBC_OCCUPY_INFO
{
	GENERATED_USTRUCT_BODY()
		FLBC_OCCUPY_INFO() {};
public:
	///等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		uint8 level;
	///名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString lbcName;

	FLBC_OCCUPY_INFO(const FVariant& variant);
};

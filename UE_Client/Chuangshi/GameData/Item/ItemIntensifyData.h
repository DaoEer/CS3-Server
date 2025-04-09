#pragma once

#include "Chuangshi.h"
#include "ItemIntensifyData.generated.h"

/**
* 文件名称：ItemIntensifyData.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-09-12
*/

UENUM(BlueprintType)
enum class EIntensifyLevel : uint8
{
	///铁星
	IronStar = 1 UMETA(DisplayName = "IronStar"),
	///铜星
	CopperStar = 2 UMETA(DisplayName = "CopperStar"),
	///银星
	SilverStar = 3 UMETA(DisplayName = "SilverStar"),
	///金星
	GoldStar = 4 UMETA(DisplayName = "GoldStar"),
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FIntensifyData
{
	GENERATED_BODY()
public:
	UPROPERTY(BlueprintReadOnly)
		FString MainPropertyStr;
	UPROPERTY(BlueprintReadOnly)
		FString AttachPropertyStr;
	UPROPERTY(BlueprintReadOnly)
		FString UID = TEXT("-1");
	UPROPERTY(BlueprintReadOnly)
		EIntensifyLevel StarLevel;
	void GetMainPropertyAndValue(FString& firstPropertyID, int32& firstValue, FString& secondPropertyID, int32& secondValue)
	{
		FString firstProperty;
		FString secondProperty;
		MainPropertyStr.Split(TEXT("|"), &firstProperty, &secondProperty);
		FString firstPropertyValue;
		FString secondPropertyValue;
		firstProperty.Split(TEXT("#"), &firstPropertyID, &firstPropertyValue);
		secondProperty.Split(TEXT("#"), &secondPropertyID, &secondPropertyValue);
		firstValue = FSTRING_TO_INT(firstPropertyValue) / 100;
		secondValue = FSTRING_TO_INT(secondPropertyValue) / 100;
	}
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FIntensifySaveData
{
	GENERATED_BODY()
public:
	UPROPERTY(BlueprintReadOnly)
		int32 index;
	UPROPERTY(BlueprintReadOnly)
		FString equipUID;
	UPROPERTY(BlueprintReadOnly)
		int32 equipID;
	UPROPERTY(BlueprintReadOnly)
		FString intensifyDataStr;
};
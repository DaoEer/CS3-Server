#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "TextShieldData.generated.h"

/**
* 文件名称：TextShieldData.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2018-01-11
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTEXT_SHIELD_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShieldText;
};


USTRUCT(BlueprintType)
struct CHUANGSHI_API FTEXT_SHIELD_TEST_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ShieldTextTest;
};

#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "ColorAliasData.generated.h"

/**
* 文件名称：ColorAliasData.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-18
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCOLOR_ALIAS_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "ColorAlias", DisplayName = "Color")
		FColor Color;
};

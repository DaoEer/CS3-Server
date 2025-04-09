#pragma once
#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "PlayerLightData.generated.h"

/**
* 文件名称：PlayerLightData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2019-09-06
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPLAYER_LIGHT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 当前关卡的光照强度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RoleBody")
		float LightIntensity = 3.0f;
	// 当前关卡的光照颜色
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "RoleBody")
		FLinearColor LightColor = FLinearColor::White;
	// 当前关卡名
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString MapName = TEXT("");
};
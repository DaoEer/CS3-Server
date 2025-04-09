#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "GameData/GameDeFine.h"
#include "RoleReviveCostData.generated.h"

/**
* 文件名称：RoleReviveCostData.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-05-21
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FROLE_REVIVE_COST_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	/// 复活类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		REVIVE_TYPE ReviveType;
	/// 复活次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReviveNumber = 0;
	/// 复活的消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReviveCost = 0;
	/// 使用复活后的CD
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReviveCoolDownTime = 0;
};

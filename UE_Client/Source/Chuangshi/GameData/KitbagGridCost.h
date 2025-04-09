#pragma once
#include "GameData/CsvTableRowBase.h"
#include "KitbagGridCost.generated.h"

/**
* 文件名称：KitbagGridCost.h
* 功能说明：背包解锁消耗配置数据
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2019-08-20
*/

/**
*表格行名为格子背包格子序号，序号1为背包所有锁定的格子都未解锁时的第一个格子。如果解锁了格子，该格子对应的序号还是不变
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FKITBAG_GRID_COST : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	///消耗金钱（可能是金币或者仙石，由策划决定，目前是仙石）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "MoneyCost")
		int32 MoneyCost;
	///消耗物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemID")
		int32 ItemID;
	///消耗物品数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ItemCost")
		int32 ItemCost;
};
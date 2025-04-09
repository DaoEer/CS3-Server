#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "LingTianPlantData.generated.h"

/**
* 文件名称：LingTianPlantData.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-05-06
*/

//生长阶段对应模型编号
USTRUCT(BlueprintType)
struct CHUANGSHI_API FGROWTHSTAGEMODELNUMBER
{
	GENERATED_BODY()
	//生长阶段
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "GrowthStage")
		int32  growthStage;
	//模型编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "ModelNumber")
		FString  modelNumber;
	//生长时间(分钟)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "GrowthStage")
		int32  growthTime;
};

///灵田上的种子生长阶段
USTRUCT(BlueprintType)
struct CHUANGSHI_API FLING_TIAN_PLANT_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	// 种子编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "SeedNum")
		int32 seedNum;
	// 物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "SeedItemID")
		int32 seedItemID;
	///需要灵田等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "NeedLevel")
		int32 needLevel;
	///种子图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "SeedIcon")
		FString seedIcon;
	///种子名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "SeedName")
		FString seedName;
	//生长阶段对应模型编号
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "PlantData", DisplayName = "GrowthStage")
		TArray<FGROWTHSTAGEMODELNUMBER> growthStageModelNumber;
	//农作物的相对位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "PosArr")
		TArray<FVector>  posArr;
};
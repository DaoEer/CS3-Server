#pragma once
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "CampMoraleReward.generated.h"

USTRUCT(BlueprintType)
struct CHUANGSHI_API FCAMP_MORALE_REWARD : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CAMP_MORALE_REWARD" , DisplayName = "morale")
		int32 morale = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CAMP_MORALE_REWARD", DisplayName = "title")
		int32 title = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CAMP_MORALE_REWARD", DisplayName = "rewardID")
		FString rewardID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "CAMP_MORALE_REWARD", DisplayName = "description")
		FString description;
};
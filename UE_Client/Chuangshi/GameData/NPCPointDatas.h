#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "NPCPointDatas.generated.h"

/**
* 文件名称：NPCPointDatas.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-08-21
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNPC_ID_TO_POSITION
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString NPCID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool Fixed;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSPACE_NPC_ID_TO_POSITION:public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FNPC_ID_TO_POSITION> NPCIDToPositions;
};

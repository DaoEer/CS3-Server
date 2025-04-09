#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "NavigatePath.generated.h"

/**
* 文件名称：NavigatePath.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-09-29
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNAVIGATE_PATH_POINT_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ID = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FVector Position;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNAVIGATE_PATH_EDGE_INFO
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Start = 0;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 End = 0;
};

USTRUCT(BlueprintType)
struct CHUANGSHI_API FNAVIGATE_PATH_INFO:public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FNAVIGATE_PATH_POINT_INFO> Points;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FNAVIGATE_PATH_EDGE_INFO> Edges;
};

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "Util/ConvertUtil.h"
#include "SpawnData.generated.h"

/**
* 文件名称：SpawnData.h
* 功能说明：刷新点 数据结构表
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2016-10-12
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSpawnData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
		FSpawnData() {}
public:
	//ScriptID
	//UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SpawnData", DisplayName = "ScriptID")
		//int32 ScriptID;

	///整体模型路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SpawnData", DisplayName = "ModelNumber")
		FString ModelNumber;

	///ModelScale
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "SpawnData", DisplayName = "ModelScale")
		float ModelScale = 0.0f;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		if (!(this->ModelNumber.IsEmpty()))
		{
			ResultInfo.Result = Ok;
			return;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("The value of ModelNumber is empty!\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};
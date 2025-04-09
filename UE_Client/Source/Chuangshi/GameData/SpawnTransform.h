#pragma once

#include "CsvTableRowBase.h"
#include "SpawnTransform.generated.h"

/**
* 文件名称：SpawnTransform.h
* 功能说明：Actor的Transform配置，用于程序代码创建的Actor
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-6-16
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSpawnTransform : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:
	//Actor的UClass
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSubclassOf<AActor> SpawnClass;

	//位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FTransform Transform;

	//描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Description;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo)
	{
		if (this->SpawnClass == nullptr)
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("The value of SpawnClass is None!\n"));
			return;
		}
		else
		{
			ResultInfo.Result = Ok;
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo)
	{
		CheckShallow(ResultInfo);
	};
};
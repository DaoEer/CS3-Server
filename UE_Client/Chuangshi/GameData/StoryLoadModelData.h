#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "StoryLoadModelData.generated.h"

/**
* 文件名称：StoryLoadModelData.h
* 功能说明：
* 文件作者：linhaowen
* 目前维护：linhaowen
* 创建时间：2019-09-16
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FSTROY_LOAD_MODEL_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:

	///需要预加载的，半身像语音ID（@DT_AudioCfg）
	///支持：
	///	播放镜头前进行资源预加载（@CST-8139）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray <FString> HeadModelID;

	///需要预加载的，模型资源列表
	///支持：
	///	骨骼网格物体、静态网格物体……等
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray <TSoftObjectPtr<UObject> > LoadModelList;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		for (int i = 0; i < LoadModelList.Num(); i++)
		{
			auto Asset = LoadModelList[i];
			if (Asset.ToSoftObjectPath().IsValid())
			{
				if (CheckIsScriptPackage(Asset.ToString()))
				{
					if (!CheckScriptSoftPtrIsValid(Asset))
					{
						ResultInfo.Result = Error;
						ResultInfo.CheckLog += FString::Printf(TEXT("; \"LoadModelList\" index(%s) resource does not exist"), i);
					}
				}
				else if (!CheckResourceFileIsExist(Asset.ToString()))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog += FString::Printf(TEXT("; \"LoadModelList\" index(%d) resource does not exist"), i);
				}
			}
			else
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog += FString::Printf(TEXT("; \"LoadModelList\" index(%d) config is None"), i);
			}
		}

		if (ResultInfo.Result == Error)
		{
			ResultInfo.CheckLog = "Error: " + ResultInfo.CheckLog.Right(ResultInfo.CheckLog.Len() - 2);
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
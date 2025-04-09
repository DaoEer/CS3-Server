#pragma once

#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "ProfessionData.generated.h"

/**
* 文件名称：ProfessionData.h
* 功能说明：角色职业配置表
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-09-20
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FProfessionData : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//阵营类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 CampType = 0;
	//职业类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ProfessionType = 0;
	//职业名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ProfessionName;
	//职业Icon贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> TexturePath;

public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;

		if (TexturePath.ToSoftObjectPath().IsValid())
		{
			if (CheckIsScriptPackage(TexturePath.ToString()))
			{
				if (!CheckScriptSoftPtrIsValid(TexturePath))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" resource does not exist"));
				}
			}
			else if (!CheckResourceFileIsExist(TexturePath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" resource does not exist"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"TexturePath\" config is None"));
		}
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
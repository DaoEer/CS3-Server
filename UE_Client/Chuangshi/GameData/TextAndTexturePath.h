#pragma once

#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "TextAndTexturePath.generated.h"

/**
* 文件名称：TextAndTexturePath.h
* 功能说明：Texture和Text配置表
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-9-20
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTextAndTexturePath : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//名称
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Text;
	//贴图路径
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
	}

	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};
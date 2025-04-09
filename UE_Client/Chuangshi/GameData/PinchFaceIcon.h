
#pragma once

#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "PinchFaceIcon.generated.h"

/**
* 文件名称：PinchFaceIcon.h
* 功能说明：捏脸数据相关
* 文件作者：zhuangzhenguo
* 目前维护：zhuangzhenguo
* 创建时间：2019-04-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FPINCHFACE_ICON_DATA : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()

public:


	///捏脸ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "IconId")
		int32  IconId;
	///捏脸分类id
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "Category")
		int32  Category;
	///性别
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "Sex")
		int32  Sex;
	///贴图路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "TexturePath")
		TSoftObjectPtr<UTexture2D> TexturePath;
	///部位种类
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "sort")
		FString sort;
	///脸部样式
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "Index")
		float  Index;
	///部位模型资源
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FPINCHFACE_ICON_DATA", DisplayName = "PartModelName")
		FString  PartModelName;

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
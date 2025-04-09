// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "GameData/CsvTableRowBase.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"
#include "StrToClass.generated.h"

/**
* 文件名称：StrToClass.j
* 功能说明：字符串与蓝图类的对应关系，用于c++创建蓝对象
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-01-17
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FStrToClass : public FCSV_TABLE_ROW_BASE
{
	GENERATED_USTRUCT_BODY()
public:
	//编号对应蓝图类路径
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftClassPtr<UObject> ClassPath;

	//后台异步加载(永不释放)
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool BackstageAsyncLoad = true;

	UClass* GetTargetClass()
	{
		UClass* targetClass = ClassPath.Get();
		if (!IsValid(targetClass) && UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->ResourceManager)
		{
			return UUECS3GameInstance::Instance->ResourceManager->SynchronousLoadClass(ClassPath);
		}
		return targetClass;
	}

	bool GetIsBackstageAsyncLoad() override
	{
		return BackstageAsyncLoad;
	};
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		ResultInfo.Result = Ok;
		if (ClassPath.ToSoftObjectPath().IsValid())
		{
			if (CheckIsScriptPackage(ClassPath.ToString()))
			{
				if (!CheckScriptSoftPtrIsValid(ClassPath))
				{
					ResultInfo.Result = Error;
					ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ClassPath\" resource does not exist!\n"));
				}
			}
			else if (!CheckResourceFileIsExist(ClassPath.ToString()))
			{
				ResultInfo.Result = Error;
				ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ClassPath\" resource does not exist!\n"));
			}
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog = FString::Printf(TEXT("Error: \"ClassPath\" config is None!\n"));
		}
	}
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	}
};

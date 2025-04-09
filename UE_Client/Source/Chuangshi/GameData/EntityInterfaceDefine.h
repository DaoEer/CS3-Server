// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "CsvTableRowBase.h"
#include "CS3Base/CS3EntityInterface.h"
#include "EntityInterfaceDefine.generated.h"

/**
* 文件名称：EntityInterfaceDefine.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：wuxiaoou
* 创建时间：2017-06-07
*/

/**
*entity的接口配置结构体
*功能：用于配置各类entity所具体的接口
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FINTERFACEDEFINE : public FCSV_TABLE_ROW_BASE
{
	GENERATED_BODY()
public:

	//加载的def定义类名称
	UPROPERTY(EditAnywhere)
		FString EntityName;

	//0加载到所有指定类,1只加载到玩家
	UPROPERTY(EditAnywhere)
		int32   Type = 0;

	//接口的UClass属性类
	UPROPERTY(EditAnywhere)
		TSubclassOf<UCS3EntityInterface> ClassEntity;

	//对应接口的名称
	UPROPERTY(EditAnywhere)
		FString ActorPropertyName;
public:
	//不会加载其他资源得浅检查
	virtual void CheckShallow(RowCheckResultInfo& ResultInfo) override
	{
		bool EntityNameResult = !EntityName.TrimStartAndEnd().IsEmpty();
		bool TypeResult = (Type == 0 || Type == 1);
		bool ClassEntityResult = true;
		if (!EntityNameResult) ResultInfo.CheckLog += FString::Printf(TEXT("EntityName cannot be empty!  "));
		if (!TypeResult) ResultInfo.CheckLog += FString::Printf(TEXT("Type value is config error!  "));
		if (IsValid(ClassEntity))
		{
			if (!CheckIsScriptPackage(ClassEntity->GetPathName()))
			{
				if (!CheckResourceFileIsExist(ClassEntity->GetPathName()))
				{
					ClassEntityResult = false;
					ResultInfo.CheckLog += FString::Printf(TEXT("ClassEntity resource does not exist!  "));
				}
			}
		}
		else
		{
			ClassEntityResult = false;
			ResultInfo.CheckLog += FString::Printf(TEXT("ClassEntity config is None!  "));
		}
		bool ActorPropertyNameResult = !ActorPropertyName.TrimStartAndEnd().IsEmpty();
		if (!ActorPropertyNameResult) ResultInfo.CheckLog += FString::Printf(TEXT("ActorPropertyName cannot be empty!  "));
		if (EntityNameResult && TypeResult && ClassEntityResult && ActorPropertyNameResult)
		{
			ResultInfo.Result = Ok;
		}
		else
		{
			ResultInfo.Result = Error;
			ResultInfo.CheckLog += FString::Printf(TEXT("\n"));
		}
	};
	//会加载其他资源得深检查(深检查中要先调用浅检查)
	virtual void CheckDeep(RowCheckResultInfo& ResultInfo) override
	{
		CheckShallow(ResultInfo);
	};
};


/**
* FINTERFACEDEFINE的列表
*/
USTRUCT(BlueprintType)
struct CHUANGSHI_API FINTERFACEDEFINEARRAY
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere)
		TArray<FINTERFACEDEFINE> items;

};
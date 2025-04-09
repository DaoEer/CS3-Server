// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/Skill/BuffData.h"
#include "GameData/Skill/BuffTableData.h"
#include "GameData/CS3Object.h"
#include "Engine/StreamableManager.h"
#include "BuffManager.generated.h"

/*
* 文件名称：BuffManager.h
* 功能说明：
* 文件作者：wangzheng
* 目前维护：wuxiaoou
* 创建时间：2017-01-05
*/

/**
 * Buff管理器
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UBuffManager : public UCS3Object
{
	GENERATED_BODY()
public:
	UBuffManager();
	~UBuffManager();

	static UBuffManager* GetInstance();

	//异步加载buff得资源
	void AsyncLoadBuffAsset(FStreamableDelegate DelegateToCall, int32 BuffID);

	/**
	*BlueprintCallable,创建buff界面数据
	*
	*@return FBuffUIData* buff数据
	*/
	FBuffUIData CreateBuffUIData(const int32& BuffIndex, const int32& BuffID, const float& BuffTotalTime, const float& BuffTime, const int32& Layer);

	/**
	*获取buff数据结构体
	*
	*@param BuffId BuffID
	*
	*@return const FBUFF_TABLE_DATA* buff数据结构体
	*/
	const FBUFF_TABLE_DATA* GetBuffDataByBuffID(int32 BuffId);

	/**
	*BlueprintPure，通过Buff ID获取Buff图标
	*
	*@param BuffId BuffID
	*
	*@return UTexture2D* Buff图标
	*/
	UFUNCTION(BlueprintPure, Category = "BuffManager")
	UTexture2D* GetIconByBuffID(int32 BuffId);

	/**
	*BlueprintPure，通过Buff ID获取Buff名称
	*
	*@param BuffId BuffID
	*
	*@return FString Buff名称
	*/
	UFUNCTION(BlueprintPure, Category = "BuffManager")
	FString GetNameByBuffID(int32 BuffId);

	/**
	* 获取持有者开关条件描述
	*/
	UFUNCTION(BlueprintPure, Category = "BuffManager")
		FString GetTargetActForbidDescribe(int32 BuffId);

/*
private:
	static UBuffManager* Instance;*/
	
};

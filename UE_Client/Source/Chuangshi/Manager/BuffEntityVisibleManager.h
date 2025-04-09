// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/BuffEntityVisibleData.h"
#include "BuffEntityVisibleManager.generated.h"

/*
* 文件名称：BuffEntityVisibleManager.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-08-23
*/

DECLARE_STATS_GROUP(TEXT("UBuffEntityVisibleManager"), STATGROUP_BuffEntityVisibleManager, STATCAT_Advanced);

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffEntityVisibleManager : public UCS3Object
{
	GENERATED_BODY()
	
public:
	UBuffEntityVisibleManager();
	~UBuffEntityVisibleManager();
	
	static UBuffEntityVisibleManager* GetInstance();

	void InitBuffVisibleTabel();

	void OnAddBuff(int32 buffID);
	void OnRemoveBuff(int32 buffID);

	UFUNCTION(BlueprintCallable, Category = "BuffEntityVisibleManager")
	VISIBLE_TYPE GetVisibleTypeByScriptID(const FString& ScriptID);

protected:
	void UpdateAroundActor(int32 buffID);


private:
	TArray<int32> BuffVisibleList;								///所有与可见性相关的buffID

	TMap<FString, FBEV_CFG_ROW_DATA> BuffVisibleDatas;			/// {scriptID : ,}

	//static UBuffEntityVisibleManager* Instance;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/QuestEntityVisibleData.h"
#include "QuestEntityVisibleManager.generated.h"

/*
* 文件名称：QuestEntityVisibleManager.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-04-28
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UQuestEntityVisibleManager : public UCS3Object
{
	GENERATED_BODY()
	
public:
	UQuestEntityVisibleManager();
	~UQuestEntityVisibleManager();

	static UQuestEntityVisibleManager* GetInstance();

	virtual void BeginDestroy() override;

	/**
	*当前任务状态下entity是否可见
	*
	*@param ScriptID: entity scriptID
	*
	*@return  不可见返回0，可见返回1，不影响返回-1
	*/
	UFUNCTION(BlueprintCallable, Category = "QuestEntityVisibleManager")
	int32 GetEntityVisible(const FString& EntityScriptID);

	///更新周围任务entity可见性
	void UpdateAroundQuestEntityVisible();

private:
	///加载某entity的配置数据
	void LoadEntityVisibleConfig(FString EntityScriptID);

private:
	TMap<FString, FQEV_ONE_ENTITY_SITUATION> ConfigDatas;
	
	/**
	 * \brief CST-10838 由于ConfigTable->GetRow<FQEV_CFG_ROW_DATA>(EntityScriptID)查询效率太低,所以这里记录已经查询过但是没有配置的
	 */
	TSet<FString> NotConfigDatas;

	//static UQuestEntityVisibleManager* Instance;
	
};

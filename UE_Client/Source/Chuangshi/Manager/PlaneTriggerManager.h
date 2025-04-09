// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "UObject/NoExportTypes.h"
#include "GameData/PlaneTrigger.h"
#include "GameData/GameDeFine.h"
#include "GameData/CS3Object.h"
#include "PlaneTriggerManager.generated.h"


/*
* 文件名称：PlaneTriggerManager.h
* 功能说明：位面触发条件判断
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-13
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UPlaneTriggerManager : public UCS3Object
{
	GENERATED_BODY()

public:
	static UPlaneTriggerManager* GetInstance();
	/**
	* 初始化位面触发数据
	*
	* @param  PlaneName		 位面名字
	*
	*@return 无
	*/
	void InitTriggerData(const FString& PlaneName);

	/**
	* 是否能进入位面
	*
	* @param  PlaneName		 位面名字
	*
	*@return bool 能进入位面返回TRUE，否则返回FALSE。
	*/
	bool CanEnterPlane(const FString& PlaneName);

private:
	UPROPERTY()
	TMap<FString, FPlaneTriggerCondition> TriggerDatas;	///位面触发条件数据

	//static UPlaneTriggerManager* Instance;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/SpaceEventCondition/SEConditionBase.h"
#include "SECondition18.generated.h"

/**
* 文件名称：SECondition18.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-02-23
*/

/**
* 玩家进入某范围事件中，判断是否在某范围中
* 注：类名需与服务器端对应
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USECondition18 : public USEConditionBase
{
	GENERATED_BODY()
		typedef USEConditionBase Supper;

public:
	/**
	*初始化触发副本剧情事件的条件数据
	*
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 圆形填1，多边形填2
	*@param Param2 圆形填中点；多边形填二维坐标列表，用竖号隔开
	*@param Param3 圆形填半径；多边形填z值上限
	*@param Param4 多边形填z值下限
	*
	*@return 无
	*/
	void InitParams(FString SpaceScriptID, INT32 EventType, INT32 EventID, FString Param1, FString Param2, FString Param3, FString Param4) override;

	/**
	*检测是否符合触发副本剧情事件的条件
	*
	*@param _entity Entity
	*@param Params 参数
	*
	*@return bool 符合触发副本剧情事件的条件返回TRUE，否则返回FALSE
	*/
	bool CheckCondition(KBEngine::Entity* _entity, TMap<FString, FString> Params) override;	
	
};

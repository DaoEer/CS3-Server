// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "KBEngine.h"
#include "SEConditionBase.generated.h"

/**
* 文件名称：SEConditionBase.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-02-23
*/

/**
 * 触发副本剧情事件的条件基类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USEConditionBase : public UCS3Object
{
	GENERATED_BODY()
	
public:
	/**
	*初始化触发副本剧情事件的条件数据
	*
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 事件参数1
	*@param Param2 事件参数2
	*@param Param3 事件参数3
	*@param Param4 事件参数4
	*
	*@return 无
	*/
	virtual void InitParams(FString SpaceScriptID, INT32 EventType, INT32 EventID, FString Param1, FString Param2, FString Param3, FString Param4);

	/**
	*检测是否符合触发副本剧情事件的条件
	*
	*@param _entity Entity
	*@param Params 参数
	*
	*@return bool 符合触发副本剧情事件的条件返回TRUE，否则返回FALSE
	*/
	virtual bool CheckCondition(KBEngine::Entity* _entity, TMap<FString, FString> Params);

public:
	INT32 EventType;///<事件类型
	INT32 EventID;///<事件ID
};

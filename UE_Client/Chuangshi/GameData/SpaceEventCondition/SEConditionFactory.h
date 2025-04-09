// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "SEConditionBase.h"
#include "SEConditionFactory.generated.h"

/**
* 文件名称：SEConditionFactory.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-02-23
*/

/**
 * SEConditionFactory类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USEConditionFactory : public UCS3Object
{
	GENERATED_BODY()
public:
	/**
	*创建触发副本剧情事件的条件类
	*
	*@param ScriptName 触发副本剧情事件的条件类脚本名字
	*
	*@return USEConditionBase* 触发副本剧情事件的条件类对象
	*/
	static USEConditionBase* CreateConditionByClass(FString ScriptName);
};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Area/BaseArea.h"
#include "UObject/NoExportTypes.h"
#include "SpaceEventBaseArea.generated.h"

/**
* 文件名称：SpaceEventBaseArea.h
* 功能说明：进入某区域触发副本剧情事件
* 文件作者：chenweilan
* 目前维护：wuxiaoou
* 创建时间：2017-02-20
*/

/**
* 触发副本剧情事件的区域
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceEventBaseArea : public UBaseArea
{
	GENERATED_BODY()

public:
	USpaceEventBaseArea();
	~USpaceEventBaseArea();

	/**
	*初始化触发副本剧情事件区域数据
	*
	*@param EventType 事件类型
	*@param EventID 事件ID
	*@param Param1 事件参数1
	*@param Param2 事件参数2
	*@param Param3 事件参数3
	*
	*@return 无
	*/
	virtual void InitParams(FString ScriptID, INT32 EventType, INT32 EventID, FString Param1, FString Param2, FString Param3);

	/**
	*进入SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	void OnEnter(const FString SpaceScriptID) override;

	/**
	*离开SpaceScriptID所对应的的区域范围函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	virtual void OnLeave(const FString SpaceScriptID) override;

	/**
	*判断当前Player是否在区域范围内
	*
	*@return bool 当前Player在区域范围内返回true，否则为false
	*/
	bool IsPlayerIn();
	
public:
	INT32 AreaIndex;	///<用于标识是哪个区域
protected:
	INT32 EventType;///<事件类型
	INT32 EventID;///<事件ID
};
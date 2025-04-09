// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "UObject/NoExportTypes.h"
#include "BaseQuestArea.generated.h"

/**
* 文件名称：BaseQuestArea.h
* 功能说明：进入某区域触发任务目标完成的区域类
* 文件作者：chentao
* 目前维护：hejingke
* 创建时间：2016-12-21

*/
/**
* 进入某区域触发任务目标完成的区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaseQuestArea : public UBaseArea
{
	GENERATED_BODY()
	
public:
	UBaseQuestArea();
	~UBaseQuestArea();

	/**
	*对任务ID和任务目标ID进行判断是否符合触发任务目标完成区域的条件
	*
	*@return bool
	*/
	bool CheckCondition();

	/**
	*判断当前Player是否在区域范围内
	*
	*@return bool 当前Player在区域范围内返回true，否则为false
	*/
	bool IsPlayerIn() override;

	/**
	*初始化区域数据
	*
	*@param QuestID 任务ID
	*@param TaskID 任务目标ID
	*@param Param1 ScriptID
	*@param Param2 区域中心点坐标的字符串
	*@param Param3 Range/100
	*
	*@return 无
	*/
	void InitDatas(int QuestID, int TaskID, const FString& Param1, const FString& Param2, const FString& Param3);

	/**
	*进入SpaceScriptID所对应的的任务区域函数
	*
	*@param SpaceScriptID 要进入任务区域的ScriptID
	*
	*@return 无
	*/
	void OnEnter(const FString SpaceScriptID) override;

public:
	int QuestID;	///< 任务ID
	int TaskID;	///<任务目标ID

protected:	
	int Range;	///< 区域范围
	FVector Point;///< 区域中心点坐标
};
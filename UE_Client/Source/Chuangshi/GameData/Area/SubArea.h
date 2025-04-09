// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "BaseArea.h"
#include "SubArea.generated.h"

/**
* 文件名称：SubArea.h
* 功能说明：地图子区域
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2016-12-28
*/

/**
* 地图子区域类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USubArea : public UBaseArea
{
	GENERATED_BODY()
	
public:
	USubArea();
	~USubArea();

	/**
	*初始化区域数据
	*
	*@param AreaRow 区域数据
	*
	*@return 无
	*/
	void InitDatas(FAREA_DATA* AreaRow);

	/**
	*进入SpaceScriptID所对应的的地图子区域函数
	*
	*@param SpaceScriptID 要进入区域的ScriptID
	*
	*@return 无
	*/
	virtual void OnEnter(const FString SpaceScriptID) override;		

	virtual SPACE_AREA_TYPE GetType() override { return SPACE_AREA_TYPE::SPACE_AREA_TYPE_SUB; };
	
	virtual void OnLeave(const FString SpaceScriptID) override;

private:
	int32 AreaPvpRule = 0;
};

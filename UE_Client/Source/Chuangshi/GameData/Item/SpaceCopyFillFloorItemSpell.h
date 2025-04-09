// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/Item/ItemUse.h"
#include "SpaceCopyFillFloorItemSpell.generated.h"

/**
* 文件名称：SpaceCopyFillFloorItemSpell.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-03-06
*/

/**
 * 物品使用类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceCopyFillFloorItemSpell : public UItemUse
{
	GENERATED_BODY()

public:
	virtual void SetUseItemToPositionBeforeNotifyServer();			///<使用对位置释放的物品前的调用(没有到服务器) 具体需求可见JIRA CST-6736
	virtual void CancelUseItemToPositionBeforeNotifyServer();		///<取消使用对位置释放的物品前的调用或者通知服务器前调用(没有到服务器)
};
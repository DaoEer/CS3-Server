// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/MonsterOptimize.h"

/*
* 文件名称：MonsterCommander.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-3-2
*/

/**
* 指挥官类型小怪
*/
class CHUANGSHI_API MonsterCommander : public MonsterOptimize
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MonsterOptimize Supper;

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

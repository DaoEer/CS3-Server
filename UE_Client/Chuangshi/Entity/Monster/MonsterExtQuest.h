// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtQuest.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2018-01-18
*/

/**
* 任务怪
*/
class CHUANGSHI_API MonsterExtQuest : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtQuest();
	~MonsterExtQuest();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

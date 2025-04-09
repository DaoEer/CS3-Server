// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtClick.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-11
*/

/**
* 可点击怪物
*/
class CHUANGSHI_API MonsterExtClick : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtClick();
	~MonsterExtClick();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
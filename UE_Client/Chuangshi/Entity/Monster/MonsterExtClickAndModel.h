// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtClickAndModel.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-25
*/


/**
* 可点击怪物
*/
class CHUANGSHI_API MonsterExtClickAndModel : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtClickAndModel();
	~MonsterExtClickAndModel();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
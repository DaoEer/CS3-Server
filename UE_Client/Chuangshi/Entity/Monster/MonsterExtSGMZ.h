// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtSGMZ.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-09-18
*/

/**
* 上古密阵BOSS
*/
class CHUANGSHI_API MonsterExtSGMZ : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtSGMZ();
	~MonsterExtSGMZ();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
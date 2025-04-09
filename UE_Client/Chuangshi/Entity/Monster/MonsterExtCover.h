// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtCover.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-5-14
*/

/**
*  轮回秘境保护罩 怪物
*/
class CHUANGSHI_API MonsterExtCover : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtCover();
	~MonsterExtCover();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

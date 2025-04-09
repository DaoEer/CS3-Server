// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：MonsterExtShareHP.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2017-09-13
*/

/**
* 血量共享怪
*/
class CHUANGSHI_API MonsterExtShareHP : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtShareHP();
	~MonsterExtShareHP();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
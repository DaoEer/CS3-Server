// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"


/*
* 文件名称：MonsterExtSFMJ.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-08-06
*/

/**
* 神风秘境 -- F键交互怪物
*/
class CHUANGSHI_API MonsterExtSFMJ : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtSFMJ();
	~MonsterExtSFMJ();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
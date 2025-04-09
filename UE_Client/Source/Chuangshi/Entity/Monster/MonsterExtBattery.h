// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtBattery.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2019-12-26
*/

/**
*  炮台
*/
class CHUANGSHI_API MonsterExtBattery : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtBattery();
	~MonsterExtBattery();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

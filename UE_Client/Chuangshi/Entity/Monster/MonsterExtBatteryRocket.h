// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/MonsterExtBattery.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtBatteryRocket.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-2-19
*/

/**
*  炮台
*/
class CHUANGSHI_API MonsterExtBatteryRocket : public MonsterExtBattery
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef MonsterExtBattery Supper;
public:
	MonsterExtBatteryRocket();
	~MonsterExtBatteryRocket();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

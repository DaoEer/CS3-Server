// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/MonsterExtAttackCityLadder.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtCollisionCar.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-3-8
*/

/**
*  撞车
*/
class CHUANGSHI_API MonsterExtCollisionCar : public MonsterExtAttackCityLadder
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef MonsterExtAttackCityLadder Supper;
public:
	MonsterExtCollisionCar();
	~MonsterExtCollisionCar();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterBuilding.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：wuxiaoou
* 创建时间：2017-07-13
*/

/**
* 移动平台
*/
class CHUANGSHI_API MonsterBuilding : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterBuilding();
	~MonsterBuilding();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
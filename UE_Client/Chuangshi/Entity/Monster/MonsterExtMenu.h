// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtMenu.h
* 功能说明：可提供菜单栏给玩家选择的怪物
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-04-20
*/

/**
*  
*/
class CHUANGSHI_API MonsterExtMenu : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtMenu();
	~MonsterExtMenu();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

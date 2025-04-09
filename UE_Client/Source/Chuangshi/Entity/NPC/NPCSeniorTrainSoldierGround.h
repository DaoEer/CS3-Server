// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPCTrainSoldierGround.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCSeniorTrainSoldierGround.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-05-15
*/

/**
* 高级练兵场
*/
class CHUANGSHI_API NPCSeniorTrainSoldierGround : public NPCTrainSoldierGround
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCTrainSoldierGround Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCSeniorTrainSoldierGround();
	~NPCSeniorTrainSoldierGround();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
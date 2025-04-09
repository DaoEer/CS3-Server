// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCTrainSoldierGround.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-04-16
*/

/**
* 练兵场
*/
class CHUANGSHI_API NPCTrainSoldierGround : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCTrainSoldierGround();
	~NPCTrainSoldierGround();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
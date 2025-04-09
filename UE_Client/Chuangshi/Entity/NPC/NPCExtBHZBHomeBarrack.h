// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCExtBHZBHomeBarrack.h
* 功能说明：帮会争霸大本营
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-07-30
*/

/**
* 帮会争霸大本营
*/
class CHUANGSHI_API NPCExtBHZBHomeBarrack : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCExtBHZBHomeBarrack();
	~NPCExtBHZBHomeBarrack();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
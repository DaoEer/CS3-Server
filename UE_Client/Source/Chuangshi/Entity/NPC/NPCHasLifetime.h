// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCHasLifetime.h
* 功能说明：有生命时间的NPC
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-7-16
*/

/**
 * CST-10782 程序内容需求（0级）——轮回秘境机缘玩法
 */
class CHUANGSHI_API NPCHasLifetime : public NPC
{
	typedef NPC Supper;
	KBE_DECLARE_ENTITY_MAP();
public:
	NPCHasLifetime();
	~NPCHasLifetime();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

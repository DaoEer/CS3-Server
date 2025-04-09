// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCNeuralShop.h
* 功能说明：英雄联盟 中立商店NPC
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2019-02-16
*/

/**
 * 英雄联盟 中立商店NPC
 */
class CHUANGSHI_API NPCNeuralShop : public NPC
{
	KBE_DECLARE_ENTITY_MAP();
	typedef NPC Supper;
public:
	NPCNeuralShop();
	~NPCNeuralShop();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

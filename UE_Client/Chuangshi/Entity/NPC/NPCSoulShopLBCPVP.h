// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCSoulShopLBCPVP.h
* 功能说明：英雄联盟商店NPC
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2020-6-30
*/

/**
 * 高级练兵场PVP NPC
 */
class CHUANGSHI_API NPCSoulShopLBCPVP : public NPC
{
	typedef NPC Supper;
	KBE_DECLARE_ENTITY_MAP();
public:
	NPCSoulShopLBCPVP();
	~NPCSoulShopLBCPVP();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

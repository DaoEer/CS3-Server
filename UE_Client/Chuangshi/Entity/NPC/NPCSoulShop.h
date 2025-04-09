// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCSoulShop.h
* 功能说明：英雄联盟商店NPC
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-07-2
*/

/**
 * 英雄联盟商店NPC
 */
class CHUANGSHI_API NPCSoulShop : public NPC
{
	typedef NPC Supper;
	KBE_DECLARE_ENTITY_MAP();
public:
	NPCSoulShop();
	~NPCSoulShop();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

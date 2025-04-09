// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCExtMysteriousShop.h
* 功能说明：神秘商人
* 文件作者：QRN
* 目前维护：QRN
* 创建时间：2020-08-18
*/

/**
 * 神秘商人
 */
class CHUANGSHI_API NPCExtMysteriousShop : public NPC
{
	KBE_DECLARE_ENTITY_MAP();
	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCExtMysteriousShop();
	~NPCExtMysteriousShop();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

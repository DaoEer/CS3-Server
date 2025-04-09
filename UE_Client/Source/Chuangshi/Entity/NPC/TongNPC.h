// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：TongNPC.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-03-23
*/

/**
 * 帮会NPC
 */
class CHUANGSHI_API TongNPC : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	TongNPC();
	~TongNPC();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

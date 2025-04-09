// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：TeleportStone.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：qiurunan
* 创建时间：2017-09-26
*/

/**
 * 传送石
 */
class CHUANGSHI_API TeleportStone : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	TeleportStone();
	~TeleportStone();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

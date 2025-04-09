// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatform.h
* 功能说明：
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-07-19
*/

/**
 * 移动平台
 */
class CHUANGSHI_API MovingPlatform : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatform();
	~MovingPlatform();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	
};

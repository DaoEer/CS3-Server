// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformTrigger.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-01-18
*/

/**
* 移动平台
*/
class CHUANGSHI_API MovingPlatformTrigger : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformTrigger();
	~MovingPlatformTrigger();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型


};
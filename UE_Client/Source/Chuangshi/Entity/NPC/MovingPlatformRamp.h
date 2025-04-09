// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/MovingPlatformShade.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformRamp.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-05-30
*/

/**
* 移动平台
*/
class CHUANGSHI_API MovingPlatformRamp : public MovingPlatformShade
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MovingPlatformShade Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformRamp();
	~MovingPlatformRamp();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型


};
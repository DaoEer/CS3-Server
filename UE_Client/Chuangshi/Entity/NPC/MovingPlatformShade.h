// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformShade.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-02-06
*/

/**
* 移动平台
*/
class CHUANGSHI_API MovingPlatformShade : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformShade();
	~MovingPlatformShade();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型


};
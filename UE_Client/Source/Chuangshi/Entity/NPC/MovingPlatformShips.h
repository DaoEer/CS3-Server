// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformShips.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-10-08
*/

/**
* 仙舟渡劫 -- 移动平台
*/
class CHUANGSHI_API MovingPlatformShips : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformShips();
	~MovingPlatformShips();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型


};
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：TongNagual.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2018-03-16
*/

/**
*  帮会神兽
*/
class CHUANGSHI_API TongNagual : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	TongNagual();
	~TongNagual();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtQQRYJ.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-08-26
*/

/**
* 巧取熔岩晶 ---骑乘推动怪
*/
class CHUANGSHI_API MonsterExtQQRYJ : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtQQRYJ();
	~MonsterExtQQRYJ();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
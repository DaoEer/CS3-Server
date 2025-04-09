// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：MonsterExtCall.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2017-05-11
*/

/**
* 移动平台
*/
class CHUANGSHI_API MonsterExtCall : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtCall();
	~MonsterExtCall();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

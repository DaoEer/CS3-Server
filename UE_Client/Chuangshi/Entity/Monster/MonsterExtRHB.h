#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：MonsterExtRotat.h
* 功能说明：
* 文件作者：lintongbin
* 目前维护：lintongbin
* 创建时间：2020-1-13
*/

/**
* 旋转怪物
*/
class CHUANGSHI_API MonsterExtRHB : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtRHB();
	~MonsterExtRHB();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

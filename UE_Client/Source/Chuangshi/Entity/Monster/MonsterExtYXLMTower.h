#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtYXLMTower.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-11-13
*/

/**
* 英雄联盟 防御塔
*/
class CHUANGSHI_API MonsterExtYXLMTower : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtYXLMTower();
	~MonsterExtYXLMTower();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

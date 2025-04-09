#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtFirstTongStarcraftBoss.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-07-30
*/

/**
*CST-7904 帮会争霸第一场 Boss怪
*/
class MonsterExtFirstTongStarcraftBoss : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtFirstTongStarcraftBoss();
	~MonsterExtFirstTongStarcraftBoss();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


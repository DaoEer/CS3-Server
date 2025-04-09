#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtRareBoss.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-07-10
*/

/**
*稀有Boss怪
*/
class MonsterExtRareBoss : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtRareBoss();
	~MonsterExtRareBoss();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtRotat.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-12
*/

/**
* 旋转怪物
*/
class CHUANGSHI_API MonsterExtRotat : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtRotat();
	~MonsterExtRotat();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

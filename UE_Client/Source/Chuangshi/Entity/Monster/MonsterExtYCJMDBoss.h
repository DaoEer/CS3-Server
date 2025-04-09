#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtYCJMDBoss.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-9-5
*/

/**
* CST-8727 勇闯夺命岛Boss
*/
class CHUANGSHI_API MonsterExtYCJMDBoss : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtYCJMDBoss();
	~MonsterExtYCJMDBoss();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

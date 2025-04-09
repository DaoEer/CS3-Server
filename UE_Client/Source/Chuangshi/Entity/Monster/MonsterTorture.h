#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterTorture.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-07-31
*/

/**
* 拷问副本专用怪物
*/
class CHUANGSHI_API MonsterTorture : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterTorture();
	~MonsterTorture();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

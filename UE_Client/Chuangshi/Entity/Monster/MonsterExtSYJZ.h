#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtSYJZ.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-07-24
*/

/**
* 三源镜柱(可点击怪物:左键单击)
*/
class CHUANGSHI_API MonsterExtSYJZ : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtSYJZ();
	~MonsterExtSYJZ();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

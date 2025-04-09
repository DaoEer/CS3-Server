#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterClientBase.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-1-19
*/

/**
* 追击怪物
*/
class CHUANGSHI_API MonsterClientBase : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterClientBase();
	~MonsterClientBase();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtJump.h
* 功能说明：跳跃怪物
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-1-26
*
*/

class CHUANGSHI_API MonsterExtJump : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtJump();
	~MonsterExtJump();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

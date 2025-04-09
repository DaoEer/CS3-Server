#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtFireCow.h
* 功能说明：火焰牛魔
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020/6/20
*/

/**
* 火焰牛魔Monster
*/
class CHUANGSHI_API MonsterExtFireCow : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtFireCow();
	~MonsterExtFireCow();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

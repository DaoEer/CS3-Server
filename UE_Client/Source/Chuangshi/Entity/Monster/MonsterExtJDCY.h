#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtJDCY.h
* 功能说明：禁地采药怪物
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020/7/4
*/

/**
* 拒马
*/
class CHUANGSHI_API MonsterExtJDCY : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtJDCY();
	~MonsterExtJDCY();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

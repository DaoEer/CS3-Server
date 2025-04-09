#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtHasCreator.h
* 功能说明：专属怪
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-13
*/
class CHUANGSHI_API MonsterExtHasCreator : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	typedef Monster Supper;
public:
	MonsterExtHasCreator();
	~MonsterExtHasCreator();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

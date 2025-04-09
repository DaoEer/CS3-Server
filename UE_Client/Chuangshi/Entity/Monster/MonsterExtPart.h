#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtPart.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-8-12
*/

/**
* 联合怪物：副怪
*/
class CHUANGSHI_API MonsterExtPart : public Monster
{

	KBE_DECLARE_ENTITY_MAP();
	typedef Monster Supper;
public:
	MonsterExtPart();
	 ~MonsterExtPart();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

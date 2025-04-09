#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtCircleEffect.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020/5/25
*/

/**
* 环形火焰Monster
*/
class CHUANGSHI_API MonsterExtCircleEffect : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtCircleEffect();
	~MonsterExtCircleEffect();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

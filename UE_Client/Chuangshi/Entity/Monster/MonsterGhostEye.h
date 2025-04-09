#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterGhostEye.h
* 功能说明：鬼瞳之眼
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2020/4/2
*/

/**
* 拒马
*/
class CHUANGSHI_API MonsterGhostEye : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterGhostEye();
	~MonsterGhostEye();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

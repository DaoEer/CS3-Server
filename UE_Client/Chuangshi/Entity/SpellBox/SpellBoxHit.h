#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBoxSpecial.h"

/*
* 文件名称：SpellBoxHit.h
* 功能说明：
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-09-20
*/

/**
* 撞击交互的SpellBox
*/
class SpellBoxHit : public SpellBoxSpecial
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBoxSpecial Supper;

public:
	SpellBoxHit();
	~SpellBoxHit();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
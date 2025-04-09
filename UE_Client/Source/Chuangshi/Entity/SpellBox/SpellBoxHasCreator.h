#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
/*
* 文件名称：SpellBoxHasCreator.h
* 功能说明：专属SpellBox
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-13
*/

class SpellBoxHasCreator : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
public:
	SpellBoxHasCreator();
	~SpellBoxHasCreator();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

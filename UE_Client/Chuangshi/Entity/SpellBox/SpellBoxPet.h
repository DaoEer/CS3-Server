#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
/*
* 文件名称：SpellBoxPet.h
* 功能说明：幻兽掉落 专属SpellBox
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-03-01
*/

class SpellBoxPet : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
public:
	SpellBoxPet();
	~SpellBoxPet();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

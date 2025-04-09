#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：SpellBoxLingTian.h
* 功能说明：灵田spellbox
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-23
*/

class SpellBoxLingTian : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef SpellBox Supper;
public:
	SpellBoxLingTian();
	~SpellBoxLingTian();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：SpellBoxAdvanced.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2018-05-16
*/

/**
* 高级SpellBox
*/
class SpellBoxAdvanced : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
DEF_INTERFACE_CONTENT()
public:
	SpellBoxAdvanced();
	~SpellBoxAdvanced();
    
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

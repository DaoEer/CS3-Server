#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：SpellBoxSpecial.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-03-30
*/

/**
* 大地图的特殊场景物件
*/
class SpellBoxSpecial : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
	DEF_INTERFACE_CONTENT()
public:
	SpellBoxSpecial();
	~SpellBoxSpecial();
};

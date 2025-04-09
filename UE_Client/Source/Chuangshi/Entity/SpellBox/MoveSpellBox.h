#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"

/*
* 文件名称：MoveSpellBox.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-09-01
*/

/**
* 可移动场景物件
*/
class MoveSpellBox : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;

public:
	MoveSpellBox();
	~MoveSpellBox();
};

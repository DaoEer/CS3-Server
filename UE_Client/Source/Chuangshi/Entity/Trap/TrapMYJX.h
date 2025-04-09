#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"

/*
* 文件名称：TrapMYJX.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-04-09
*/

/**
CST-6526 冥域缉凶 弹射机关陷阱
*/
class TrapMYJX : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;

public:
	TrapMYJX();
	~TrapMYJX();

};

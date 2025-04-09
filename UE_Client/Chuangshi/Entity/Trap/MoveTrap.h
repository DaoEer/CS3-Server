#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MoveTrap.h
* 功能说明：
* 文件作者：wuxiaoou
* 目前维护：wuxiaoou
* 创建时间：2017-07-07
*/

/**
移动类陷阱
*/
class MoveTrap : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;
	DEF_INTERFACE_CONTENT()
public:
	MoveTrap();
	~MoveTrap();


};

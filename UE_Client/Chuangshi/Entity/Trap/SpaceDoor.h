#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"

/*
* 文件名称：SpaceDoor
* 功能说明：
* 文件作者：chenweilan
* 目前维护：wuxiaoou
* 创建时间：2017-11-02
*/

/**
*大地图传送门
*/
class SpaceDoor : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;

public:
	SpaceDoor();
	~SpaceDoor();

};

#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtLightWall.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2018-03-07
*/

/**
* 光墙，CST-3248
*/
class CHUANGSHI_API MonsterExtDemonGuard :	public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtDemonGuard();
	~MonsterExtDemonGuard();
};


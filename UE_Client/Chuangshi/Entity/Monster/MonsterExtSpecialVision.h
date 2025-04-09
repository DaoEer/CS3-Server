#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtSpecialVision.h
* 功能说明：
* 文件作者：lintongbin
* 目前维护：lintongbin
* 创建时间：2019-12-23
*/

/**
* 
*/
class CHUANGSHI_API MonsterExtSpecialVision : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtSpecialVision();
	~MonsterExtSpecialVision();
};


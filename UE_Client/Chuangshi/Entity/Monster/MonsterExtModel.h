#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtModel.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-10-18
*/

/**
* Monster，有独立模型支持
*/
class CHUANGSHI_API MonsterExtModel : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtModel();
	~MonsterExtModel();

};

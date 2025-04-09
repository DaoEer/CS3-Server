#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"
/*
* 文件名称：MonsterExtRevive.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-03-22
*/

/**
*复活怪，在一定时间内可能会复活
*/
class MonsterExtRevive : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtRevive();
	~MonsterExtRevive();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtCanPush.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-10-08
*/

/**
* 可推动怪物
*/
class CHUANGSHI_API MonsterExtCanPush : public Monster
{

	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtCanPush();
	 ~MonsterExtCanPush();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

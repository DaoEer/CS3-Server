#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtArmorLock.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-10-19
*/

class CHUANGSHI_API MonsterExtArmorLock : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtArmorLock();
	virtual ~MonsterExtArmorLock();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


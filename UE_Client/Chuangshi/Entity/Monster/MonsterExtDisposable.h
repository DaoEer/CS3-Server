#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtDisposable.h
* 功能说明：一次性的随从怪物
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-11-10
*/

class CHUANGSHI_API MonsterExtDisposable : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtDisposable();
	~MonsterExtDisposable();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

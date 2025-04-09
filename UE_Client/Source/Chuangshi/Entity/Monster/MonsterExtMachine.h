#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtMachine.h
* 功能说明：
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2017-08-09
*/

/**
* 机关怪 （炮台，滚石）
*/
class CHUANGSHI_API MonsterExtMachine : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtMachine();
	~MonsterExtMachine();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

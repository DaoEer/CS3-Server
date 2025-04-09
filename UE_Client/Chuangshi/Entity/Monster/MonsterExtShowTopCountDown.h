#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtShowTopCountDown.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-4-23
*/

/**
* 头顶显示倒计时怪
*/
class CHUANGSHI_API MonsterExtShowTopCountDown : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtShowTopCountDown();
	~MonsterExtShowTopCountDown();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

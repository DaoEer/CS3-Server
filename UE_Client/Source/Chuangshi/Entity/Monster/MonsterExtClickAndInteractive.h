#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtClickAndInteractive.h
* 功能说明：用来做既可以双击又可以F交互的怪物
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2020-5-26
*/

class CHUANGSHI_API MonsterExtClickAndInteractive : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtClickAndInteractive();
	~MonsterExtClickAndInteractive();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
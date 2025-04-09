#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtTiShen.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-04-23
*/

/**
* 替身Monster，复制玩家外观和血量等
*/
class CHUANGSHI_API MonsterExtTiShen : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtTiShen();
	~MonsterExtTiShen();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

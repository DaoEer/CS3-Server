#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtXinMo.h
* 功能说明：
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2017-06-06
*/

/**
* 心魔Monster，复制玩家外观和技能
*/
class CHUANGSHI_API MonsterExtXinMo : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtXinMo();
	~MonsterExtXinMo();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

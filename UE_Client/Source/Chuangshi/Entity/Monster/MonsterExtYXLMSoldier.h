#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtYXLMSoldier.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2018-11-12
*/

/**
* 英雄联盟 小兵
*/
class CHUANGSHI_API MonsterExtYXLMSoldier : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtYXLMSoldier();
	~MonsterExtYXLMSoldier();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtLingMai.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2018-03-20
*/

/**
* 灵脉战场BOSS
*/
class CHUANGSHI_API MonsterExtLingMai :	public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()

	typedef Monster Supper;
public:
	MonsterExtLingMai();
	~MonsterExtLingMai();

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


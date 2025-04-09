#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtRefreshTime.h
* 功能说明：
* 文件作者：lintongbin
* 目前维护：lintongbin
* 创建时间：2019-7-23
*/

class CHUANGSHI_API MonsterExtRefreshTime : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	typedef Monster Supper;
public:
	MonsterExtRefreshTime();
	virtual ~MonsterExtRefreshTime();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtJingShiDongKu.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-12-20
*/

/**
* 晶石洞窟副本专用怪物
*/
class CHUANGSHI_API MonsterExtJingShiDongKu : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtJingShiDongKu();
	~MonsterExtJingShiDongKu();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

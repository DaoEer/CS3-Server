#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtXuanTianBaoLu.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-02-20
*/

/**
* 玄天宝录副本 旋转怪物支持
*/
class CHUANGSHI_API MonsterExtXuanTianBaoLu : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtXuanTianBaoLu();
	~MonsterExtXuanTianBaoLu();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

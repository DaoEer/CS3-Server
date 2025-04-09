#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"

/*
* 文件名称：SpellBoxPickItem.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-10-26
*/

/**
* 场景物件玩家自主选择物品
*/
class SpellBoxPickItem : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;

public:
	SpellBoxPickItem();
	~SpellBoxPickItem();

protected:
	virtual void OnEnterWorld() override;      ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;      ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

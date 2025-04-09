#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"

/*
* 文件名称：SpellBoxPlunderBox.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2020-9-08
*/

/**
* 帮会掠夺战 宝箱
*/
class SpellBoxPlunderBox : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;

public:
	SpellBoxPlunderBox();
	~SpellBoxPlunderBox();

protected:
	virtual void OnEnterWorld() override;      ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;      ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

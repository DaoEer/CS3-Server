#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：DropBox.h
* 功能说明：
* 文件作者：huangshijie
* 目前维护：wuxiaoou
* 创建时间：2016-10-18
*/

/**
*掉落物品类
*/
class DropBox : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;

public:
	DropBox();
	~DropBox();

protected:
	virtual void OnEnterWorld() override;      ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;      ///< 当Entity离开世界（被销毁时）时，此方法被调用

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
DEF_INTERFACE_CONTENT()
};
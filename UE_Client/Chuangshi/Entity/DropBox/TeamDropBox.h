#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：TeamDropBox.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-11-13
*/

/**
*队伍宝箱
*/
class TeamDropBox : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;

public:
	TeamDropBox();
	~TeamDropBox();

protected:
	virtual void OnEnterWorld() override;      ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;      ///< 当Entity离开世界（被销毁时）时，此方法被调用

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
DEF_INTERFACE_CONTENT()
};
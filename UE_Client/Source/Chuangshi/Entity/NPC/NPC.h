#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPC.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

/**
*NPC对象基础类
*所有扩展出的NPC对象都应该继承于该类
*/

class NPC : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;

public:
	NPC();
	~NPC();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

DEF_INTERFACE_CONTENT()
};
#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：SpellBox.h
* 功能说明：
* 文件作者：chenweilai
* 目前维护：wuxiaoou
* 创建时间：2017-04-26
*/


class AServerCharacter;
/**
*场景物件对象类
*/

class SpellBox : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;

DEF_INTERFACE_CONTENT()
public:
	SpellBox();
	~SpellBox();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	virtual void OnBindActorToEntity()override;
};

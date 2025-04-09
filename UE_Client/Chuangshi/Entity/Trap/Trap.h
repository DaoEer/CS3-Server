#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：Trap.h
* 功能说明：
* 文件作者：huangshijie
* 目前维护：wuxiaoou
* 创建时间：2017-01-09
*/

/**
*陷阱对象类
*所有扩展出的怪物对象都应该继承于该类
*非移动类
*/
class Trap : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;
	DEF_INTERFACE_CONTENT()
public:
	Trap();
	~Trap();

public:
	void OnActorCreaterFinish(int32 entityId);///<对像创建完成时调用
	virtual bool IsState(ENTITY_STATE EntityState) override;///<Entity状态

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	

};
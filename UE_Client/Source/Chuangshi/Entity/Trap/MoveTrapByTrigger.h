#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MoveTrapByTrigger.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2017-10-17
*/

/**
移动类陷阱
*/
class MoveTrapByTrigger : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;
	DEF_INTERFACE_CONTENT()
public:
	MoveTrapByTrigger();
	~MoveTrapByTrigger();


public:

	virtual UClass* GetEntityModelClassAsset() override;
};

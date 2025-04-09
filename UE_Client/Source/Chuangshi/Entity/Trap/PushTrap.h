#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：PushTrap.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-25
*/

/**
推人陷阱类
*/
class PushTrap : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;
	DEF_INTERFACE_CONTENT()
public:
	PushTrap();
	~PushTrap();

public:
	virtual UClass* GetEntityModelClassAsset() override;

};

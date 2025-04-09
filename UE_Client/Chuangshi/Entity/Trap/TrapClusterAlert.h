#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：TrapClusterAlert.h
* 功能说明：
* 文件作者：chenweilai
* 目前维护：wuxiaoou
* 创建时间：2017-04-07
*/

/**
集群怪统一警戒陷阱，客户端循环检测范围内是否有玩家
*/
class TrapClusterAlert : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;
	DEF_INTERFACE_CONTENT()
public:
	TrapClusterAlert();
	~TrapClusterAlert();

};

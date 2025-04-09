#pragma once
#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCTorture.h
* 功能说明：拷问副本特殊NPC
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-07-16
*/

class NPCTorture : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCTorture();
	~NPCTorture();


protected:

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
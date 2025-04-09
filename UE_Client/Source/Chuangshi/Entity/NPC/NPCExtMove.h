#pragma once
#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：NPCExtMove.h
* 功能说明：
* 文件作者：gaoruilian
* 目前维护：wuxiaoou
* 创建时间：2017-09-27
*/

class NPCExtMove : public NPC
{
	typedef NPC Supper;
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
public:
	NPCExtMove();
	~NPCExtMove();


protected:

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
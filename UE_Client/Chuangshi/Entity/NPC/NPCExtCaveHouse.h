
#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"


/*
* 文件名称：NPCExtCaveHouse.h
* 功能说明：轮回秘境洞府
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-03-19
*/

/**
* 详情请见JIRA：CST-5774
*/

class CHUANGSHI_API NPCExtCaveHouse :public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;

	DEF_INTERFACE_CONTENT()
public:
	NPCExtCaveHouse();
	~NPCExtCaveHouse();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

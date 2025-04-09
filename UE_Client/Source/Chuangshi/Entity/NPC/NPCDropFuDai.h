
#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"
#include "CS3Base/InterfaceDef.h"


/*
* 文件名称：NPCDropFuDai.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-12-01
*/

/**
* 详情请见JIRA：CST-5774
*/

class CHUANGSHI_API NPCDropFuDai :public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;
	DEF_INTERFACE_CONTENT()
public:
	NPCDropFuDai();
	~NPCDropFuDai();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

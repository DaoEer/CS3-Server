#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCChangeBody.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2017-09-06
*/

/**
* 变身比赛NPC
*/

class NPCChangeBody : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;

public:
	NPCChangeBody();
	~NPCChangeBody();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
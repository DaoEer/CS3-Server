#pragma once

#include "KBEngine.h"
#include "Entity/NPC/NPC.h"

/*
* 文件名称：NPCExtCompose.h
* 功能说明：轮回秘境打造NPC
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-07-08
*/



class NPCExtCompose : public NPC
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPC Supper;

public:
	NPCExtCompose();
	~NPCExtCompose();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
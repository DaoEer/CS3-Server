#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtLightWall.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2018-03-07
*/

/**
* 光墙，CST-3248
*/
class CHUANGSHI_API MonsterExtLightWall :	public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtLightWall();
	~MonsterExtLightWall();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


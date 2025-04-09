#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtChartlet.h
* 功能说明：
* 文件作者：zhutianyang
* 目前维护：zhutianyang
* 创建时间：2018-03-20
*/

/**
* 画卷贴图
*/
class CHUANGSHI_API MonsterExtChartlet :	public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtChartlet();
	~MonsterExtChartlet();

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


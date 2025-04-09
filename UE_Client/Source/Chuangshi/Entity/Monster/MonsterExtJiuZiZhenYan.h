#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtJiuZiZhenYan.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2018-06-20
*/

/**
* 九字真言副本(真言)
*/
class CHUANGSHI_API MonsterExtJiuZiZhenYan : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtJiuZiZhenYan();
	~MonsterExtJiuZiZhenYan();

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtJZZYXY.h
* 功能说明：
* 文件作者：qiurunan
* 目前维护：qiurunan
* 创建时间：2020-03-11
*/

/**
* 真言虚影(九字真言)
*/
class CHUANGSHI_API MonsterExtJZZYXY : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtJZZYXY();
	~MonsterExtJZZYXY();

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

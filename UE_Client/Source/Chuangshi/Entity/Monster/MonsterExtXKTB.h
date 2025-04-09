#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtXKTB.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2020-04-10
*/

/**
* 虚空探宝
*/
class CHUANGSHI_API MonsterExtXKTB : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtXKTB();
	~MonsterExtXKTB();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


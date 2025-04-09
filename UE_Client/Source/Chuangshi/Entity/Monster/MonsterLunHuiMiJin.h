#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterLunHuiMiJin.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-12-24
*/

/**
* 上古密阵匹配怪物
*/
class CHUANGSHI_API MonsterLunHuiMiJin : public Monster
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterLunHuiMiJin();
	~MonsterLunHuiMiJin();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


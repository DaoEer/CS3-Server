#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtMiZhen.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-09-20
*/

/**
* 上古密阵匹配怪物
*/
class CHUANGSHI_API MonsterExtMiZhen : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtMiZhen();
	~MonsterExtMiZhen();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


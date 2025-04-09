#pragma once
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtWXHJ.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-07-08
*/

/**
* 五行画卷
*/
class CHUANGSHI_API MonsterExtWXHJ : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtWXHJ();
	~MonsterExtWXHJ();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtFenHuoJinNiu.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-01-08
*/

/**
* 环任务副本 焚火金牛怪
*/
class CHUANGSHI_API MonsterExtFenHuoJinNiu : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtFenHuoJinNiu();
	~MonsterExtFenHuoJinNiu();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

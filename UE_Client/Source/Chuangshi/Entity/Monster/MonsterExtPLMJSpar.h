#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"

/*
* 文件名称：MonsterExtPLMJSpar.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-3-13
*/

/**
* CST-6262 蟠龙秘境 奇晶
*/
class CHUANGSHI_API MonsterExtPLMJSpar : public Monster
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Monster Supper;
public:
	MonsterExtPLMJSpar();
	~MonsterExtPLMJSpar();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

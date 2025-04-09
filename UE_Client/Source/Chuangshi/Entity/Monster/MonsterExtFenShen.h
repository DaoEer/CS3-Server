#pragma once

#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterExtFenShen.h
* 功能说明：
* 文件作者：QRN
* 目前维护：QRN
* 创建时间：2020-09-07
*/

/**
* 分身
*/
class CHUANGSHI_API MonsterExtFenShen : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterExtFenShen();
	~MonsterExtFenShen();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

};

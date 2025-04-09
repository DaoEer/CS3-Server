#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBoxSpecial.h"

/*
* 文件名称：SpellBoxDoor.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-09-27
*/

/**
* 范围检测交互的SpellBox
*/
class SpellBoxDoor : public SpellBoxSpecial
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBoxSpecial Supper;

public:
	SpellBoxDoor();
	~SpellBoxDoor();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
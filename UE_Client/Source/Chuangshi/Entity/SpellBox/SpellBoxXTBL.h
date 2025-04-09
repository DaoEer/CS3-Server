#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
/*
* 文件名称：SpellBoxXTBL.h
* 功能说明：玄天宝录副本 专属SpellBox
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2019-02-20
*/

class SpellBoxXTBL : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
public:
	SpellBoxXTBL();
	~SpellBoxXTBL();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

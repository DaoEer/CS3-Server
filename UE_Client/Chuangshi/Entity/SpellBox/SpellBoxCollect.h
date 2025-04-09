#pragma once

#include "KBEngine.h"
#include "Entity/SpellBox/SpellBox.h"
/*
* 文件名称：SpellBoxCollect.h
* 功能说明：采集spellbox
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-04-02
*/

class SpellBoxCollect : public SpellBox
{
	KBE_DECLARE_ENTITY_MAP();

	typedef SpellBox Supper;
public:
	SpellBoxCollect();
	~SpellBoxCollect();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

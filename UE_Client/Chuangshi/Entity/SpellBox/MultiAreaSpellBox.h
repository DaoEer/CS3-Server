#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"

/*
* 文件名称：MultiAreaSpellBox.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-18
*/

/**
* 多区域触发Entity
*/
class MultiAreaSpellBox : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef NPCBaseObject Supper;

public:
	MultiAreaSpellBox();
	~MultiAreaSpellBox();

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};

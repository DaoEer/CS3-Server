#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/InterfaceDef.h"
/**
* GhostReceiver：定义一个傀儡受术者
*/


class GhostReceiver : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;

public:
	GhostReceiver();
	~GhostReceiver();



	virtual bool IsState(ENTITY_STATE EntityState) override;///<Entity状态

protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
DEF_INTERFACE_CONTENT()
};
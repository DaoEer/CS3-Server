#pragma once

#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"


/*
* 文件名称：Monster.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

/**
*怪物对象基础类
*所有扩展出的怪物对象都应该继承于该类
*/
class UBehaviourInterface;
class UMonsterCombatInterface;

class Monster : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef NPCBaseObject Supper;

public:
	Monster();
	~Monster();

public:
	UBehaviourInterface* BehaviourInterface = nullptr;
	UMonsterCombatInterface* CombatInterface = nullptr;

	virtual void InitInterfaceCache() override;
	virtual void DestroyInterfaces() override;

	virtual bool IsState(ENTITY_STATE EntityState) override;///<Entity状态
	
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型

	virtual void OnMoveOver(const uint32 movingID, const bool isSuccess);

public:
	void RPC_CELL_ChangeMonsterParent(KBEngine::FVariantArray Args);

	float AvoidanceConsiderationRadius = 0;
	void Set_useRVOAvoidance(const uint8& newVal, const uint8& oldVal);
};



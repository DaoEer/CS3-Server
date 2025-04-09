#pragma once

#include "CoreMinimal.h"
#include "KBEngine.h"
#include "Entity/Monster/Monster.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MonsterOptimize.h
*/
class UMonsterOptimizeInterface;
/**
* 优化怪物
*/
class CHUANGSHI_API MonsterOptimize : public Monster
{
	KBE_DECLARE_ENTITY_MAP()
	DEF_INTERFACE_CONTENT()
	typedef Monster Supper;
public:
	MonsterOptimize();
	~MonsterOptimize();
	virtual void InitInterfaceCache() override;
	virtual void DestroyInterfaces() override;

	virtual void OnMoveOver(const uint32 movingID, const bool isSuccess) override;

	UMonsterOptimizeInterface* GameObjectInterface = nullptr;
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
	virtual void Set_Position(const FVector &oldVal) override;///<设置位置
};

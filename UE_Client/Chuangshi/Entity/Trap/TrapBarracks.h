#pragma once

#include "KBEngine.h"
#include "Entity/Trap/TrapBattleFlag.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：TrapBarracks.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-28
*/

/**
兵营
*/
class TrapBarracks : public TrapBattleFlag
{
	KBE_DECLARE_ENTITY_MAP();

	typedef TrapBattleFlag Supper;
	DEF_INTERFACE_CONTENT()
public:
	TrapBarracks();
	~TrapBarracks();
public:
	virtual UClass* GetEntityModelClassAsset() override;

};

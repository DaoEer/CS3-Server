#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"

/*
* 文件名称：TrapBattleFlag.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2020-02-26
*/

/**
攻城梯战旗
*/
class TrapBattleFlag : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;

public:
	TrapBattleFlag();
	~TrapBattleFlag();
public:
	virtual UClass* GetEntityModelClassAsset() override;

};

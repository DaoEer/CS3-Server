#pragma once

#include "KBEngine.h"
#include "Entity/Trap/Trap.h"

/*
* 文件名称：TrapSymbolJade.h
* 功能说明：
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2020-05-19
*/

/**
陷阱符玉
*/
class TrapSymbolJade : public Trap
{
	KBE_DECLARE_ENTITY_MAP();

	typedef Trap Supper;

public:
	TrapSymbolJade();
	~TrapSymbolJade();
public:
	virtual UClass* GetEntityModelClassAsset() override;

};

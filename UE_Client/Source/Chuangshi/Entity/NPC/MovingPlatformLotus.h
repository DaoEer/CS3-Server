#pragma once
#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformLotus.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-03-29
*/

/*
*莲叶移动平台
*/
class MovingPlatformLotus : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();
	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformLotus();
	~MovingPlatformLotus();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


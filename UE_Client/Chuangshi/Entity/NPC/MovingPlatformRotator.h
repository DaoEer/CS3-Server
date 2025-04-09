#pragma once
#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformRotator.h
* 功能说明：
* 文件作者：wujiannan
* 目前维护：wujiannan
* 创建时间：2018-10-15
*/

/*
旋转类型移动平台
*/
class MovingPlatformRotator : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();
	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformRotator();
	~MovingPlatformRotator();


protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};


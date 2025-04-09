#pragma once
#include "KBEngine.h"
#include "Entity/NPC/MovingPlatform.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：MovingPlatformVehicle.h
* 功能说明：多人可移动骑乘
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建 2020/9/8
*/

class CHUANGSHI_API MovingPlatformVehicle : public MovingPlatform
{
	KBE_DECLARE_ENTITY_MAP();

	typedef MovingPlatform Supper;
	DEF_INTERFACE_CONTENT()
public:
	MovingPlatformVehicle();
	~MovingPlatformVehicle();
	virtual void OnLeaveWorld() override;
	void OnStartControl(int32 InDriverID);
	void OnStopControl();
protected:
	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
private:
	int32 ControlID;
};
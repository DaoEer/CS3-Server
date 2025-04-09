#pragma once


#include "KBEngine.h"
#include "Entity/NPCBaseObject.h"
#include "CS3Base/InterfaceDef.h"

/*
* 文件名称：VehiclePet.h
* 功能说明：
* 文件作者：chengdongyong
* 目前维护：chengdongyong
* 创建时间：2017-07-11
*/

/*
* 幻兽类
*/

class VehiclePet : public NPCBaseObject
{
	KBE_DECLARE_ENTITY_MAP();

	typedef NPCBaseObject Supper;
	DEF_INTERFACE_CONTENT()
public:
	VehiclePet();
	~VehiclePet();

public:
	
	/**
	*创建对象
	*
	*
	*@return 无
	*/
	virtual void DoCreateCharacter() override;

	virtual bool IsState(ENTITY_STATE EntityState) override;///<Entity状态
protected:
	//virtual void OnUpdateVolatileData() override; ///<同步位置朝向信息

	virtual UClass* GetEntityModelClassAsset() override;///< 获取Entity模型
};
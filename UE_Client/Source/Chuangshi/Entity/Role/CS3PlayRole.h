#pragma once

#include "KBEngine.h"
#include "Entity/Role/CS3Role.h"
#include "CS3Base/InterfaceDef.h"


class CHUANGSHI_API CS3PlayRole : public CS3Role
{
	KBE_DECLARE_ENTITY_MAP()
		DEF_INTERFACE_CONTENT()
		typedef CS3Role Supper;
public:
	CS3PlayRole();
	~CS3PlayRole();
	virtual void OnLeaveScenes() override;
protected:
	virtual void __init__() override;
	virtual void OnDestroy() override;
	virtual void OnEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用
	
private:
	bool bIsLeavingWorld = false; ///<是否正在离开世界(主要处理本地玩家离开世界时底层 会调用OnLeaveScenes方法，OnLeaveScenes方法中有解绑entity与Actor方法，会导致流程不正确，当前暂时采用使用该变量来处理OnLeaveScenes是否需要执行UnBindActorToEntity)
};
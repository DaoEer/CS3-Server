#pragma once

#include "KBEngine.h"
#include "CS3Base/GameObject.h"

/*
* 文件名称：NPCBaseObject.h
* 功能说明：
* 文件作者：hejingke
* 目前维护：hejingke
* 创建时间：2016-08-31 STATGROUP_CS3_NPCBaseEntity
*/

DECLARE_STATS_GROUP(TEXT("CS3_NPCBaseEntity"), STATGROUP_CS3_NPCBaseEntity, STATCAT_Advanced);

class AServerCharacter;
/**
*非玩家对象基础类
*所有扩展出的非玩家对象对象都应该继承于该类
*/
class NPCBaseObject : public GameObject
{
	KBE_DECLARE_ENTITY_MAP();
	typedef GameObject Supper;

public:
	NPCBaseObject();
	~NPCBaseObject();	

	virtual void OnSet_flags(const int64 &newValue, const int64 &oldValue) override;///<设置模型标志的回调
	/**
	/**
	*同步玩家位置
	*
	*@param newValue ，新的值（int64）
	*@param newValue ，旧的值（int64）
	*
	*@return 无
	*/
	virtual void SetSyncPosClient(const int32 &newValue, const int32 &oldValue);

	/**
	*是否准备好创建对象
	*CST-2933 台子上的怪物，需要先创建好台子，然后再创建怪物
	*
	*@return 无
	*/
	virtual bool IsReadyCreateActor();

	/**
	*创建对象
	*
	*
	*@return 无
	*/
	virtual void DoCreateCharacter() override;
	

	virtual void OnBindActorToEntity()override;

	/**
	*进入场景调用
	*
	*
	*@return 无
	*/
	virtual void OnEnterScenes() override;


protected:

	virtual void OnEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用

	void InitVolatileData();

	
private:	

	void StartSyncPosTimer(float interval);///< 开始同步定时器
	void StopSyncPosTimer();///<停止同步定时器
	bool HasSyncPosTimer();///<是否开启了同步定时器
	void SyncPosToServer();///<将位置信息同步到服务器

private:
	FTimerHandle SyncPosTimerHandle_;	     ///< 同步位置到服务器timer
	FTimerHandle DetectParentTimerHandle;	///< 检测台子的创建
};


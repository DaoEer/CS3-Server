#pragma once

#include "KBEngine.h"
#include "CS3Entity.h"
#include "GameData/SpaceEntityRelation/SpaceEntityRelation.h"
#include "GameData/GameDefine.h"
#include "ScriptModule.h"
#include "Entity/Alias.h"
#include "GameData/CharacterData.h"

/*
* 文件名称：GameObject.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

class AServerCharacter;

/**
*游戏对象基础类
*所有扩展出的游戏对象都应该继承于该类
*/
class GameObject : public CS3Entity
{
	KBE_DECLARE_ENTITY_MAP();
	typedef CS3Entity Supper;

public:

	GameObject();
	~GameObject();
	/**
	*设置模型标志
	*
	*@param newValue ，新的值（int64）
	*@param newValue ，旧的值（int64）
	*
	*@return 无
	*/
	virtual void Set_flags(const int64 &newValue, const int64 &oldValue);
	virtual void OnSet_flags(const int64 &newValue, const int64 &oldValue);

	virtual void Set_appearanceColor(const int32 &newValue, const int32 &oldValue);

	virtual UClass* GetEntityModelClassAsset();///< 获取实体模型的类

	virtual void BindActorToEntity(AServerCharacter* InServerCharacter, bool bHasBegunPlay = false) override;
	virtual void OnBindActorToEntity();		///<绑定Actor到Entity的回调
	virtual void UnBindActorToEntity()override;
	void CELL_onClientReady();

	void CreateCharacter();
	virtual void DoCreateCharacter() {};
	/**
	*该EntityID是否是玩家自己
	*
	*@param entityID ，（int32）
	*
	*@return bool 如果是，则返回True，反之返回False
	*/
	bool IsPlayerID(int32 entityID);

	/**
	*获取服务器坐标
	*
	*
	*@return FVector，坐标
	*/
	FVector GetServerSetPos() { return ServerSetPos; }

	/**
	*设置服务器坐标
	*
	*
	*@param Vector ，坐标（FVector&）
	*
	*@return 无
	*/
	void SetServerSetPos(const FVector &Vector) {  ServerSetPos = Vector; }

	/**
	*获取对象名字
	*
	*
	*@return FString&
	*/
	const FString& GetActorName();

	/**
	*获取组件名字
	*
	*
	*@return FName&
	*/
	//const FName& GetCompontentName();

	/*打开服务器同步位置
	*
	*
	*@return 无
	*/
	void OpenSyncServerPos() { SyncServerPos_ = true; }
	/**
	*关闭服务器同步位置
	*
	*
	*@return 无
	*/
	void CloseSyncServerPos() { SyncServerPos_ = false; }
	/**
	*是否同步服务器位置
	*
	*
	*@return 无
	*/
	bool IsSyncServerPos() { return SyncServerPos_; }

	///判断关系
	COMBAT_RELATION QueryRelation(KBEngine::Entity* TargetEntity);

	///获取关系判断实例
	virtual URelationBase* GetEntityRelationIns();

	virtual bool IsState(ENTITY_STATE EntityState);///<Entity状态

	FORCEINLINE const FVector &LocalDirection();

	///获取模型部件数据
	FAModelInfo GetModelInfo();

	///<获取服务器存储的单个模型部件数据，通过部件类型
	FString GetPartIdByType(MODEL_PART_TYPE PartType);
protected:
	virtual void OnEnterWorld() override;       ///< Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;       ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void Set_Position(const FVector &oldVal) override;///<设置位置
	virtual void Set_Direction(const FVector &oldVal) override;///<设置距离
	virtual void OnUpdateVolatileData() override;
	virtual void OnUpdateVolatileDataByParent() override;	//同步父对象位置方向数据
	virtual void OnGotParentEntity() override;		//获得父对象回调
	virtual void OnLoseParentEntity() override;		//失去父对象回调
	
	FString _fActorName;///<对象名称
	//FName _fCompontentName;///<组件名称

	FVector NewCharacterDirection;		// 默认情况下，character的pitch、roll 为0。需要开启IsDirectionSameToEntity
	bool IsDirectionSameToEntity = false;		

private:
	FVector ServerSetPos; ///<服务器设置的位置（目前只有在第一次设置位置的时候，由于Actor可能还没加载，用来保存服务器传过来的位置）
	bool SyncServerPos_ = true;

	
};



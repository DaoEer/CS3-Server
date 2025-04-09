#pragma once

#include "KBEngine.h"

#include "GameData/ChatType.h"
#include "Entity/Alias.h"
#include "Interface/Role/RoleRankInterface.h"
#include "CS3Base/GameObject.h"
#include "GameData/BigmapActInfo.h"
#include "GameData/CacheMsg.h"
#include "CS3Base/InterfaceDef.h"

#include "time.h"

/*
* 文件名称：Role.h
* 功能说明：
* 文件作者：liushuang
* 目前维护：wuxiaoou
* 创建时间：2016-08-29
*/

DECLARE_STATS_GROUP(TEXT("CS3_RoleEntity"), STATGROUP_CS3_RoleEntity, STATCAT_Advanced);

class AServerCharacter;
class APlayerCharacter;

/**
*玩家类
*/
class CS3Role : public GameObject
{
	KBE_DECLARE_ENTITY_MAP();
	DEF_INTERFACE_CONTENT()
	typedef GameObject Supper;

public:
	CS3Role();
	~CS3Role();


	virtual void OnSet_flags(const int64 &newValue, const int64 &oldValue) override;

	virtual void OnEnterScenes();///<当玩家第一次进入游戏，地图加载完毕后的回调函数

	/**
	*客户端从游戏状态返回到登陆界面/直接退出
	*
	*@return 无
	*/
	void Logoff();

	/**
	*客户端从游戏状态返回到角色选择
	*
	*@return 无
	*/
	void Logout();

	/**
	*通知服务器客户端某个地图已经加载完毕
	*
	*bFirst 为True时，是玩家第一次进入游戏 场景加载完毕的回调，为False时，是玩家非第一次、场景加载完毕的回调
	*
	*@return 无
	*/
	void LoadSpaceCompleted();

	/**
	*请求服务器将已出战的幻兽传送到玩家身边
	*@return 无
	*/
	void RequestPetTeleporToOwner();

	///获取关系判断实例
	virtual URelationBase* GetEntityRelationIns() override;
	virtual bool IsState(ENTITY_STATE EntityState) override;///<Entity状态

	/**
	*获取实体目标（指针）
	*
	*
	*@return 实体指针
	*/
	int32 GetTargetEntityID(); 
	void SetTargetEntityID(int32 InTargetEntityID);

#pragma region 网络
	void networkTest();
	void OnNetworkTest();
#pragma endregion
private:
	int64 networkTestRecord = 0;

protected:
	virtual void OnDestroy() override;
	virtual void OnEnterWorld() override;     ///< 当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld() override;     ///< 当Entity离开世界（被销毁时）时，此方法被调用

	/**
	*初始化entity属性接口
	*
	*@param scriptModule:一个entity.def中定义的脚本模块的描述类,包含了某个entity定义的属性与方法以及该entity脚本模块的名称与模块ID
	*
	*@return 无
	*/
	virtual void InitProperties(KBEngine::ScriptModule& scriptModule) override;


	virtual void OnBindActorToEntity() override;
	virtual void DoCreateCharacter() override;

private:
	virtual UClass* GetEntityModelClassAsset() override;///<获取玩家的Actor蓝图类资源

private:
	bool bFirstEnterSpace = true;     ///<第一次进入游戏地图（地图加载完成） 
	int32 TargetEntityID;///<实体目标ID


/* -------------------- entity属性、方法通知 ------------------------*/
private:
	int32 _camp;
	int32 _gender; 
	int64 _money;
	int32 _potential;
	FString _playerName;
	int32 _profession;
	int32 _state;
	int16 _level;
	uint64 _PlayerDBID;
	

public:
	inline void Set_Camp(const int32& newVal, const int32& oldVal) { _camp = newVal; }
	inline void Set_Gender(const int32& newVal, const int32& oldVal) { _gender = newVal; }
	inline void Set_Money(const int64& newVal, const int64& oldVal) { _money = newVal; }
	inline void Set_Potential(const int32& newVal, const int32& oldVal) { _potential = newVal; }
	inline void Set_PlayerName(const FString& newVal, const FString& oldVal) { _playerName = newVal; }
	inline void Set_Profession(const int32& newVal, const int32& oldVal) { _profession = newVal; }
	inline void Set_State(const int32& newVal, const int32& oldVal) { _state = newVal; }
	inline void Set_Level(const int16& newVal, const int16& oldVal);
	inline void Set_PlayerDBID(const uint64& newVal, const uint64& oldVal) { _PlayerDBID = newVal; }

	inline int32 Camp(){ return _camp; }
	inline int32 Gender() { return _gender; }
	inline int64 Money() { return _money; }
	inline int32 Potential() { return _potential; }
	inline FString PlayerName() { return _playerName; }
	inline int32 Profession() { return _profession; }
	inline int32 State() { return _state; }
	inline int16 Level() { return _level; }
	inline uint64 PlayerDBID() { return _PlayerDBID; }
};
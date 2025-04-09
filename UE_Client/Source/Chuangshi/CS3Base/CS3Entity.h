#pragma once
#include "KBEngine.h"
#include "Engine/EngineTypes.h"
#include "GameData/CacheMsg.h"
#include "Containers/List.h"
#include "GameData/EntityDataCache.h"
#include "InterfaceDef.h"

/*
* 文件名称：CS3Entity.h
* 功能说明：
* 文件作者：shenbing
* 目前维护：wuxiaoou
* 创建时间：2017-04-13
*/

UENUM(BlueprintType)
enum class CS3EntityStatus : uint8
{
	Created = 0,	///已创建好
	InitFinished,	///初始化完成
	BindedActor,   ///绑定了Actor
	ActorInitFinished,///Actor绑定完成
	UnBindedActor	///解绑Actor
};

DECLARE_STATS_GROUP(TEXT("CS3Entity"), STATGROUP_CS3Entity, STATCAT_Advanced);

class AServerCharacter;
class UCS3EntityInterface;

/**
*CS3Entity基类
*/
class CS3Entity : public KBEngine::Entity
{
	KBE_DECLARE_ENTITY_MAP();
	typedef Entity Supper;

public:
	CS3Entity();
	~CS3Entity();
	virtual void __init__() override;///<Entity初始化完成

			
	virtual void OnEnterScenes();///<开始场景
	virtual void OnLeaveScenes();///<离开场景
	virtual void OnEnterWorld();///<当Entity进入世界时，此方法被调用
	virtual void OnLeaveWorld();///<当Entity离开世界（被销毁时）时，此方法被调用
	
	virtual void OnDestroy();

	bool IsPlayerRole(); ///<是否是玩家自己
	bool IsPlayerAccount(); ///<是否是当前客户端账号

	/**
	*通过属性名查询值
	*
	*@param name 属性名
	*
	*@return FVariant 属性值(查询不到返回 FVariant(NULL) )
	*/
	virtual FVariant GetDefinedProperty(FString name) override;

	/**
	*转发消息到接口
	*
	*@param name 将要调用的消息名字
	*@param args 数据（TArray）
	*
	*@return 无
	*/
	virtual void OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args) override;

	void ProcessRemoteMethodCall(const FString& name, const TArray<FVariant>& args);

	virtual void BaseCall(const FString &methodname, const FVariantArray &arguments) override;
	virtual void CellCall(const FString &methodname, const FVariantArray &arguments) override;

	/**
	*获取到参数
	*
	*@param val ，参数引用（FVariant &）
	*
	*@return FString
	*/
	static const FString GetArgumentsString(const FVariant &val);

	/**
	*更新参数
	*
	*@param name ，参数名字（FString &）
	*@param newVal ，新的参数（FVariant &）
	*@param oldVal ，旧的参数（FVariant &）
	*
	*@return FString
	*/
	void OnUpdateProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal);
	
	void ProcessUpdateProperty(const FString& name, const FVariant& newVal, const FVariant& oldVal);
	/**
	*初始化参数
	*
	*@param scriptModule ，脚本组件（ScriptModule &）
	*
	*@return 无
	*/
	virtual void InitProperties(KBEngine::ScriptModule& scriptModule) override;


	/**
	*将Actor绑定到对应的Entity上
	*
	*@param actor ，actor（const AActor*）
	*
	*@return 无
	*/
	void CallActorFunc(const FString &name, const TArray<FVariant> &args);

	virtual void BindActorToEntity(AServerCharacter* InServerCharacter, bool bHasBegunPlay = false);
	void  OnActorCreateApperanceFinished(); ///<Actor外观创建完成改变Entity状态

	virtual void BindActorToInterface(AServerCharacter* InServerCharacter);

	virtual void UnBindActorToInterface();

	/**
	*将Actor和对应的Entity解除绑定
	*
	*@return 无
	*/
	virtual void UnBindActorToEntity(){ }

	//在Actor未创建时缓存远程调用方法参数
	virtual void CacheRemoteFuncParams(const FString &name, const TArray<FVariant> &args);
	//在Actor未创建时缓存远程调用方法参数
	virtual void CachePropertyUpdateParams(const FString& name, const FVariant& newVal, const FVariant& oldVal);
	//处理缓存消息
	void DealCacheMsgs();

	//TArray<FVariant> 参数 转换成 CallFunctionByNameWithArguments 的参数
	static void Parameter_FVariantToFString(const TArray<FVariant> &InParameter, FString &OutParameter);

	void SetEntityStatus(CS3EntityStatus NewStatus) { CurStatus = NewStatus; };
	CS3EntityStatus GetEntityStatus() { return CurStatus; };
	bool NoRoleStoreFuction(FString name);

public:
	CS3EntityStatus CurStatus;
	TArray<CS3EntityMessage> CacheMsgs; //Actor未创建时，缓存它的网络消息;
	TArray<FString> RoleStoreNames;

//接口消息转发
public:
	TMap< FString, UCS3EntityInterface* > m_interfaceContainer = {};
	//void InitInterfaces();

	
	UCS3EntityInterface* GetInterfaceByName(const FString& name);///< 获取相应interface
	virtual void InitInterfaceCache();
	virtual void DestroyInterfaces();
	struct FEntityInterface_Cache Interface_Cache;
protected:
	virtual const INTERFACE_DEF_MAP GetDefInterfaces() { return {}; }
	virtual void InitInterfaces() {};
};

// 对网络消息进行平滑处理,防止突然大量网络消息处理导致的卡顿
class CS3Entity_MessageSmoothing
{
public:
	static CS3Entity_MessageSmoothing& Get();
	void ProcessMessageQueue();
	void PushProcessMessage();

	void Enqueue_RemoteMethodCall(const int32 entityId, const FString& name, const TArray<FVariant>& args);
	void Enqueue_UpdateProperty(const int32 entityId, const FString& name, const FVariant& newVal, const FVariant& oldVal);

private:
	TDoubleLinkedList<CS3EntityMessage> MessageQueue;

private:
	// 禁止外部构造
	CS3Entity_MessageSmoothing();

	// 禁止外部析构
	~CS3Entity_MessageSmoothing();

	// 禁止外部复制构造
	CS3Entity_MessageSmoothing(const CS3Entity_MessageSmoothing& signal);

	// 禁止外部赋值操作
	const CS3Entity_MessageSmoothing& operator=(const CS3Entity_MessageSmoothing& signal);
};
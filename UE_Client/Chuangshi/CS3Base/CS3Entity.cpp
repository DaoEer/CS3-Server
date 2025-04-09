#include "CS3Entity.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/CacheMsg.h"
#include "Actor/ServerCharacter.h"
#include "CS3EntityInterface.h"
#include "Manager/ResourceManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Manager/LevelManager.h"
#include <exception>
#include <stdexcept>
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/GameStatus.h"

#include "Interface/StateInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Interface/EntitySpaceEventInterface.h"
#include "Interface/CombatInterface.h"

DECLARE_CYCLE_STAT(TEXT("CS3Entity_InitProperties"), STAT_CS3Entity_InitProperties, STATGROUP_CS3Entity);
DECLARE_CYCLE_STAT(TEXT("CS3Entity_BindActorToInterface"), STAT_CS3Entity_BindActorToInterface, STATGROUP_CS3Entity);
DECLARE_CYCLE_STAT(TEXT("CS3Entity_GetInterfaceObject"), STAT_CS3Entity_GetInterfaceObject, STATGROUP_CS3Entity);

DECLARE_CYCLE_STAT(TEXT("CS3Entity_MessageSmoothingProcess"), STAT_CS3Entity_MessageSmoothingProcess, STATGROUP_CS3Entity);
DECLARE_CYCLE_STAT(TEXT("CS3Entity_MessageSmoothing"), STAT_CS3Entity_MessageSmoothing, STATGROUP_CS3Entity);

KBE_BEGIN_ENTITY_METHOD_MAP(CS3Entity, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(CS3Entity, Supper)
KBE_END_ENTITY_PROPERTY_MAP()

CS3Entity::CS3Entity()
{
	SetEntityStatus(CS3EntityStatus::Created);
}

CS3Entity::~CS3Entity()
{
	CS3_Log(TEXT("Destroy EntityID[%d], Name[%s]"), ID(), *ClassName());
}

void CS3Entity::__init__()
{
	Supper::__init__();
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->__init__();
	}
}

bool CS3Entity::IsPlayerRole()
{
	if (IsPlayer() && ClassName() == TEXT("Role"))
	{
		return true;
	}
	return false;
}

bool CS3Entity::IsPlayerAccount()
{
	if (IsPlayer() && ClassName() == TEXT("Account"))
	{
		return true;
	}
	return false;
}

void CS3Entity::OnEnterScenes()
{
	CS3_Log(TEXT("Entity[%d] OnEnterScenes!"), ID());
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->OnEnterScenes();
	}
}

void CS3Entity::OnLeaveScenes()
{
	CS3_Log(TEXT("Entity[%d] OnLeaveScenes!"), ID());
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->OnLeaveScenes();
	}
}

void CS3Entity::OnEnterWorld()
{
	CS3_Log(TEXT("CS3Entity::OnEnterWorld classname[%s],[%d]"), *ClassName(), ID());
	Supper::OnEnterWorld();

	if (!IsPlayer())
	{
		UUECS3GameInstance::Instance->LevelManager->RequestEnterScenes(this);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Entity[%d] RequestEnterScenes"), ID());
	}

	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->onEnterWorld();
	}
}

void CS3Entity::OnLeaveWorld()
{
	CS3Entity_MessageSmoothing::Get().PushProcessMessage();

	CS3_Log(TEXT("CS3Entity::OnLeaveWorld classname[%s],[%d]"), *ClassName(), ID());
	Supper::OnLeaveWorld();
	OnLeaveScenes();
	UnBindActorToInterface();
	UnBindActorToEntity();
	if (this != nullptr && IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->ClearObjectHandles(this);
	}
}


void CS3Entity::OnDestroy()
{
	CS3Entity_MessageSmoothing::Get().PushProcessMessage();
}

FVariant CS3Entity::GetDefinedProperty(FString name)
{
	FVariant returnValue;
	try
	{
		returnValue = Entity::GetDefinedProperty(name);
	}
	catch (int32 errorCode)
	{
		CS3_Warning(TEXT("CS3Entity::GetDefinedProperty(%s)  errorCode:%d"), *name, errorCode);
		returnValue = FVariant(NULL);
	}
	return returnValue;
}
 
void CS3Entity::Parameter_FVariantToFString(const TArray<FVariant> &InParameter, FString &OutParameter)
{
	for (int i = 0; i < InParameter.Num(); i++)
	{
		FVariant Val = InParameter[i];
		switch (Val.GetType())
		{
		case EVariantTypes::Float:
		case EVariantTypes::UInt8:
		case EVariantTypes::UInt16:
		case EVariantTypes::UInt32:
		case EVariantTypes::Int8:
		case EVariantTypes::Int16:
		case EVariantTypes::Int32:
		{
			OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
		case EVariantTypes::String:
		{
			FString value = InParameter[i];
			if ((i + 1) == InParameter.Num())
				OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			else
				OutParameter = *FString::Printf(TEXT("%s \"%s\""), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
		default:
			OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
	}
}


bool CS3Entity::NoRoleStoreFuction(FString name)
{
	if (RoleStoreNames.Num()>0)
	{
		for (FString val: RoleStoreNames)
		{
			if (name.Equals(val))
				return true;
		}
		return false;
	}
	else
	{
		RoleStoreNames.Add("CLIENT_OnUpdateStoreGoods");
		RoleStoreNames.Add("CLIENT_OnGetRecommentGoods");
		RoleStoreNames.Add("CLIENT_OnGetStoreNewGoods");
		RoleStoreNames.Add("CLIENT_OnUpdateBuyRecords");
		RoleStoreNames.Add("CLIENT_OnUpdatePresentRecords");
		RoleStoreNames.Add("CLIENT_OnRequestPresentGift");
		RoleStoreNames.Add("CLIENT_OnUpdateGiftBox");
		RoleStoreNames.Add("CLIENT_UpdateStoreCart");
		RoleStoreNames.Add("CLIENT_OnGetGoodsListByIDList");
		RoleStoreNames.Add("AddHasStoreAppearance");
		RoleStoreNames.Add("AddStoreAppearance");
		RoleStoreNames.Add("RemoveStoreAppearance");
		RoleStoreNames.Add("UpdateStoreBackAdornParam");
		RoleStoreNames.Add("OnUpdateStoreAppearance");
		RoleStoreNames.Add("statusMessage");
		RoleStoreNames.Add("inquireMessage");
		RoleStoreNames.Add("OnStoreBuyComplete");
		return NoRoleStoreFuction(name);
	}
}

void CS3Entity::OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args)
{
	// 消息平滑处理
	{
		// 由于经过详细测试,发现还是会由于和kbe引擎层面的协议之间有顺序冲突导致奇怪的问题,暂时关闭分帧
		/*CS3Entity_MessageSmoothing& MessageSmoothing = CS3Entity_MessageSmoothing::Get();
		MessageSmoothing.Enqueue_RemoteMethodCall(ID(), name, args);*/
	}
	ProcessRemoteMethodCall(name, args);
}

void CS3Entity::ProcessRemoteMethodCall(const FString& name, const TArray<FVariant>& args)
{
	// KBE的协议转发
	Supper::OnRemoteMethodCall(name, args);

	//在Actor没有初始化完成前，把消息缓存起来
	AActor* CS3Actor = Actor();
	if (!IsValid(CS3Actor)&& !UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::ChangeClothes))
	{
		CacheRemoteFuncParams(name, args);
		return;
	}

	//当世界状态处于ChangeClothes时 只允许RoleStore的服务器消息通过 为了解决客户端纯关卡没有entity绑定的通信问题
	if (UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::ChangeClothes))
	{

		if (!NoRoleStoreFuction(name))
		{
			return;
		}
	}

	//广播接口远程消息
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->OnRemoteMethodCall(name, args);
	}

	//给entity的actor转发
	CallActorFunc(name, args);

	KbeRpc_Info(TEXT("EntityID : %d ---- RpcName : %s ---- ClassName : %s"), ID(), *name, *ClassName());
}

const FString CS3Entity::GetArgumentsString(const FVariant &val)
{
	if (val.GetType() == EVariantTypes::Float)
	{
		float value = val;
		return FString::SanitizeFloat(value);
	}
	else if (val.GetType() == EVariantTypes::UInt8)
	{
		int32 value = (int32)val.GetValue<UINT8>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::UInt16)
	{
		int32 value = (int32)val.GetValue<UINT16>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::UInt32)
	{
		int32 value = (int32)val.GetValue<UINT32>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int8)
	{
		int32 value = (int32)val.GetValue<INT8>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int16)
	{
		int32 value = (int32)val.GetValue<INT16>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int32)
	{
		int32 value = val;
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::String)
	{
		FString value = val;
		return value;
	}
	else if (val.GetType() == EVariantTypes::Vector)
	{
		FVector value = val;
		return *FString::Printf(TEXT("(x=%f,y=%f,z=%f)"), value.X, value.Y, value.Z);
	}
	else if (val.GetType() == static_cast<EVariantTypes>(KBEngine::EKBEVariantTypes::VariantArray))
	{		
		FString ret = TEXT("(");
		KBEngine::FVariantArray value = val;
		for (int j = 0; j < value.Num(); j++)
		{
			if ((value[j]).GetType() == EVariantTypes::String)
			{
				if (j == 0)
				{
					ret = *FString::Printf(TEXT("%s\"%s\""), *ret, *GetArgumentsString(value[j]));
				}
				else
				{
					ret = *FString::Printf(TEXT("%s,\"%s\""), *ret, *GetArgumentsString(value[j]));
				}
			}
			else
			{
				if (j == 0)
				{
					ret = *FString::Printf(TEXT("%s%s"), *ret, *GetArgumentsString(value[j]));
				}
				else
				{
					ret = *FString::Printf(TEXT("%s,%s"), *ret, *GetArgumentsString(value[j]));
				}
			}
		}
		ret = *FString::Printf(TEXT("%s)"), *ret);
		return ret;
	}

	return TEXT("");
}

void CS3Entity::OnUpdateProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal)
{
	// 消息平滑处理
	{
		// 由于经过详细测试,发现还是会由于和kbe引擎层面的协议之间有顺序冲突导致奇怪的问题,暂时关闭分帧
		/*CS3Entity_MessageSmoothing& MessageSmoothing = CS3Entity_MessageSmoothing::Get();
		MessageSmoothing.Enqueue_UpdateProperty(ID(), name, newVal, oldVal);*/
	}
	ProcessUpdateProperty(name, newVal, oldVal);
}

void CS3Entity::ProcessUpdateProperty(const FString& name, const FVariant& newVal, const FVariant& oldVal)
{
	try
	{
		//在Actor没有初始化完成前，把消息缓存起来
		if (!IsValid(Actor()))
		{
			CachePropertyUpdateParams(name, newVal, oldVal);
			return;
		}

		Supper::OnUpdateProperty(name, newVal, oldVal);
		//更新注册对象的属性
		for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
		{
			it.Value()->OnUpdateProperty(name, newVal, oldVal);
		}
	}
	catch (const std::exception & e)
	{
		CS3_Warning(TEXT("Exception: CS3Entity::OnUpdateProperty name:%s reason:%s"), *name, e.what());
	}
	catch (...)
	{
		CS3_Warning(TEXT("Exception: CS3Entity::OnUpdateProperty name:%s reason:unknown"), *name);
	}


	KbeProperty_Info(TEXT("EntityID : %d ---- PropertyName : %s ---- ClassName : %s"), ID(), *name, *ClassName());
}

void CS3Entity::InitProperties(KBEngine::ScriptModule& scriptModule)
{
	CS3_Log(TEXT("CS3Entity::InitProperties begin classname[%s],[%d]"), *ClassName(), ID());
	{
		SCOPE_CYCLE_COUNTER(STAT_CS3Entity_InitProperties);
		//初始化entity的接口
		InitInterfaces();
	}
	Supper::InitProperties(scriptModule);
	SetEntityStatus(CS3EntityStatus::InitFinished);
	CS3_Log(TEXT("CS3Entity::InitProperties end classname[%s],[%d]"), *ClassName(), ID());
}

void CS3Entity::CallActorFunc(const FString &name, const TArray<FVariant> &args)
{
	FOutputDeviceNull ar;
	try
	{
		if (IsValid(Actor()))
		{
			FString FStringParameter(name);
			Parameter_FVariantToFString(args, FStringParameter);
			Actor()->CallFunctionByNameWithArguments(*FStringParameter, ar, NULL, true);
		}

	}
	catch (const std::exception &e)
	{
		CS3_Warning(TEXT("Exception: CS3Entity::OnRemoteMethodCall name:%s reason:%s"), *name, e.what());
	}
	catch (...)
	{
		CS3_Warning(TEXT("Exception: CS3Entity::OnRemoteMethodCall name:%s reason:unknown"), *name);
	}
}

void CS3Entity::BindActorToEntity(AServerCharacter * InServerCharacter, bool bHasBegunPlay)
{
	CS3_Log(TEXT("CS3Entity::BindActorToEntity classname[%s],[%d]"), *ClassName(),ID());
}

void CS3Entity::OnActorCreateApperanceFinished()
{
	SetEntityStatus(CS3EntityStatus::ActorInitFinished);
}

void CS3Entity::BindActorToInterface(AServerCharacter* InServerCharacter)
{
	CS3_Log(TEXT("CS3Entity::BindActorToInterface classname[%s],[%d]"), *ClassName(),ID());
	SCOPE_CYCLE_COUNTER(STAT_CS3Entity_BindActorToInterface);
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		FName ActorPropertyName = FName(*it->Key);
		UObjectProperty *EntitiesProp = FindField<UObjectProperty>(Actor()->GetClass(), ActorPropertyName);
		if (EntitiesProp != nullptr)
		{
			EntitiesProp->SetPropertyValue_InContainer(Actor(), it.Value());
		}
		it.Value()->SetActor(Actor());
	}
}


void CS3Entity::UnBindActorToInterface()
{
	CS3_Log(TEXT("CS3Entity::UnBindActorToInterface classname[%s],[%d]"), *ClassName(),  ID());
	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		it.Value()->onLeaveWorld();
		it.Value()->SetActor(nullptr);
	}
	DestroyInterfaces();
}

void CS3Entity::CacheRemoteFuncParams(const FString &name, const TArray<FVariant> &args)
{
	Message_RemoteMethodCall NewRemoteMethodCall{ name, args };
	CS3EntityMessage NewEntityMessage{ ID(), MoveTemp(NewRemoteMethodCall) };
	CacheMsgs.Add(NewEntityMessage);
}

void CS3Entity::CachePropertyUpdateParams(const FString& name, const FVariant& newVal, const FVariant& oldVal)
{
	Message_UpdateProperty NewUpdateProperty{ name, newVal, oldVal };
	CS3EntityMessage NewEntityMessage{ ID(), MoveTemp(NewUpdateProperty) };
	CacheMsgs.Add(NewEntityMessage);
}

void CS3Entity::DealCacheMsgs()
{
	//处理在Actor未创建时缓存的消息
	if (CacheMsgs.Num() > 0)
	{
		for (auto& item : CacheMsgs)
		{
			item.Process();
		}
		CacheMsgs.Empty();
		CS3_Display(CS3DebugType::CL_Entity, TEXT("Entity[%d] end to deal Cache OnRemoteMethodCall megs!"), ID());
	}
}

void CS3Entity::InitInterfaceCache()
{

	//CS3_Log(TEXT("UCS3EntityInterface::Load End EntityID[%d],Name[%s]"), ID(), TEXT( ClassName() ));

	// 初始化Interface_Cache

	UCS3EntityInterface** CS3EntityInterface = nullptr;

	CS3EntityInterface = m_interfaceContainer.Find("StateInterface");
	if (CS3EntityInterface) Interface_Cache.StateInterface = Cast<UStateInterface>(*CS3EntityInterface);

	CS3EntityInterface = m_interfaceContainer.Find("SkillInterface");
	if (CS3EntityInterface) Interface_Cache.SkillInterface = Cast<USkillInterface>(*CS3EntityInterface);

	CS3EntityInterface = m_interfaceContainer.Find("GameObjectInterface");
	if (CS3EntityInterface) Interface_Cache.GameObjectInterface = Cast<UGameObjectInterface>(*CS3EntityInterface);

	CS3EntityInterface = m_interfaceContainer.Find("RoleTeamInterface");
	if (CS3EntityInterface) Interface_Cache.RoleTeamInterface = Cast<URoleTeamInterface>(*CS3EntityInterface);

	CS3EntityInterface = m_interfaceContainer.Find("EntitySpaceEventInterface");
	if (CS3EntityInterface) Interface_Cache.EntitySpaceEventInterface = Cast<UEntitySpaceEventInterface>(*CS3EntityInterface);

	CS3EntityInterface = m_interfaceContainer.Find("CombatInterface");
	if (CS3EntityInterface) Interface_Cache.CombatInterface = Cast<UCombatInterface>(*CS3EntityInterface);
}

void CS3Entity::DestroyInterfaces()
{
	Interface_Cache = FEntityInterface_Cache();

	CS3_Log(TEXT("EntityID[%d] DestroyInterfaces Begin"), ID());
	TArray<UObject*> ReferredToObjs;

	for (auto it = m_interfaceContainer.CreateConstIterator(); it; ++it)
	{
		int32 count = UGolbalBPFunctionLibrary::GetObjReferenceCount(it.Value(), ReferredToObjs);

		if (count > 0)
		{
			for (UObject* Each : ReferredToObjs)
			{
				if (Each)
				{
					CS3_Warning(TEXT("failed to destory interface, EntityID[%d], Name[%s]"), ID(), *Each->GetName());
				}
			}
		}
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("EntityID[%d] Interface Name[%s] RemoveFromRoot "), ID(), *(it.Value()->GetName()));
		it.Value()->RemoveFromRoot();
	}

	m_interfaceContainer.Empty();
	CS3_Log(TEXT("EntityID[%d] DestroyInterfaces End"), ID());
}



UCS3EntityInterface* CS3Entity::GetInterfaceByName(const FString& name)
{
	if (this != nullptr && m_interfaceContainer.Contains(name))
	{
		return m_interfaceContainer[name];
	}
	return nullptr;
}

CS3Entity_MessageSmoothing& CS3Entity_MessageSmoothing::Get()
{
	static CS3Entity_MessageSmoothing MessageSmoothing;
	return MessageSmoothing;
}

void CS3Entity_MessageSmoothing::ProcessMessageQueue()
{
	SCOPE_CYCLE_COUNTER(STAT_CS3Entity_MessageSmoothing);

	const double FrameMaxProcessTime = 0.003;	// 这里控制每帧最大处理时间(单位/秒)
	static double NowFrameMaxProcessTime = FrameMaxProcessTime;

	const double StartTime = FPlatformTime::Seconds();
	bool isFrameMaxProcess = false;
	while (MessageQueue.Num() != 0)
	{
		//实际执行网络消息
		{
			auto& EntityMessage = MessageQueue.GetTail()->GetValue();

			{
				SCOPE_CYCLE_COUNTER(STAT_CS3Entity_MessageSmoothingProcess);
				if (!EntityMessage.Process())
				{
					MessageQueue.RemoveNode(MessageQueue.GetTail());
					continue;
				}
			}

			MessageQueue.RemoveNode(MessageQueue.GetTail());
		}

		const double ElapsedTime = FPlatformTime::Seconds() - StartTime;
		if (ElapsedTime >= NowFrameMaxProcessTime && UUECS3GameInstance::Instance->GameStatus != nullptr && UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::InWorld)
		{
			NowFrameMaxProcessTime += 0.0001;  //防止消息一直太多处理不过来
			isFrameMaxProcess = true;
			break;
		}
	}

	if (!isFrameMaxProcess)
	{
		NowFrameMaxProcessTime = FMath::Max(NowFrameMaxProcessTime - 0.0005, FrameMaxProcessTime);  //消息不堆积了,逐渐还原每帧最大处理时间
	}
}

void CS3Entity_MessageSmoothing::PushProcessMessage()
{
	for (auto now = MessageQueue.GetTail(); now != nullptr; now = now->GetPrevNode())
	{
		auto& EntityMessage = now->GetValue();

		EntityMessage.Process();
	}

	MessageQueue.Empty();
}

void CS3Entity_MessageSmoothing::Enqueue_RemoteMethodCall(const int32 entityId, const FString& name, const TArray<FVariant>& args)
{
	Message_RemoteMethodCall NewRemoteMethodCall{ name, args };
	CS3EntityMessage NewEntityMessage{ entityId, MoveTemp(NewRemoteMethodCall) };
	MessageQueue.AddHead(NewEntityMessage);
}

void CS3Entity_MessageSmoothing::Enqueue_UpdateProperty(const int32 entityId, const FString& name, const FVariant& newVal, const FVariant& oldVal)
{
	Message_UpdateProperty NewUpdateProperty{ name, newVal, oldVal };
	CS3EntityMessage NewEntityMessage{ entityId, MoveTemp(NewUpdateProperty) };
	MessageQueue.AddHead(NewEntityMessage);
}

CS3Entity_MessageSmoothing::CS3Entity_MessageSmoothing()
{
}

CS3Entity_MessageSmoothing::~CS3Entity_MessageSmoothing()
{
}

void CS3Entity::BaseCall(const FString &methodname, const FVariantArray &arguments)
{
	Supper::BaseCall(methodname, arguments);
	KbeRpc_Info(TEXT("EntityID : %d ---- BaseCallRpcName : %s ---- ClassName : %s"), ID(), *methodname, *ClassName());
}

void CS3Entity::CellCall(const FString &methodname, const FVariantArray &arguments)
{
	Supper::CellCall(methodname, arguments);
	KbeRpc_Info(TEXT("EntityID : %d ---- CellCallRpcName : %s ---- ClassName : %s"), ID(), *methodname, *ClassName());
}

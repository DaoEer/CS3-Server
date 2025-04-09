// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3EntityInterface.h"

#include "CS3Base/CS3Entity.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ResourceManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"
#include "Manager/CfgManager.h"


CS3_INTERFACE_METHOD_MAP UCS3EntityInterface::_thisMethodMap;
CS3_INTERFACE_PROPERTY_MAP UCS3EntityInterface::_thisPropertyMap;

UCS3EntityInterface::UCS3EntityInterface()
{

}
UCS3EntityInterface::~UCS3EntityInterface()
{

}


void UCS3EntityInterface::PostInitProperties()
{
	Super::PostInitProperties();
	OwnerActor = nullptr;
}

AActor *UCS3EntityInterface::GetActor()
{
	if (GetEntity() != nullptr && IsValid(OwnerActor))
	{
		return OwnerActor;
	}
	return nullptr;
}

bool UCS3EntityInterface::SetActor(const AActor *Actor)
{
	OwnerActor = (AActor *)Actor;
	return true;
}

KBEngine::Entity *UCS3EntityInterface::GetEntity()
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("--UCS3EntityInterface::GetEntity no this pKBEApp"));
		return nullptr;
	}
	return UUECS3GameInstance::pKBEApp->FindEntity(EntityID);
}

CS3Entity *UCS3EntityInterface::GetMyEntity()
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("--UCS3EntityInterface::GetMyEntity no this pKBEApp"));
		return nullptr;
	}
	KBEngine::Entity *e = UUECS3GameInstance::pKBEApp->FindEntity(EntityID);
	if (e) 
	{
		return static_cast<CS3Entity*>(e);
	}
	else
	{
		return nullptr;
	}

}

bool UCS3EntityInterface::SetEntityID(int32 entID)
{
	EntityID = entID;
	return true;
}

//初始化kbe插件与蓝图的通信
void UCS3EntityInterface::InitBlueCB()
{
	//初始化kbe调蓝图的方法
	ArrBlueFunc.Add("CLIENT_SetFloatPropertyByKey");
	ArrBlueFunc.Add("CLIENT_SetFStringPropertyByKey");
	ArrBlueFunc.Add("CLIENT_SetBoolPropertyByKey");

	//初始化entity属性被改变后，通知蓝图的方法回调
	//ArrBluePropertyCB.Add();

}

void UCS3EntityInterface::OnUpdateProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal)
{
	NotifyDefineProperty(name, newVal, oldVal);
	CallPropertyChangeToBlue(name, newVal, oldVal);
}

void UCS3EntityInterface::OnRemoteMethodCall(const FString &name, const TArray<FVariant> &args)
{
	CallDefineMethod(name, args);
	//调用篮图方法
	if (ArrBlueFunc.Contains(name))
	{
		CallFuncToBlueArgs( name, args  );
	}
}

void UCS3EntityInterface::CellCallWithBp(const FString &methodname, const TArray<FString> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::CellCall(EntityID, methodname, arguments);
	}
}

void UCS3EntityInterface::CellCall(const FString& name, const KBEngine::FVariantArray& args)
{
	//GetEntity()
	KBEngine::Entity* e = GetEntity();
	if (e)
		e->CellCall(name, args);
}

void UCS3EntityInterface::BaseCall(const FString& name, const KBEngine::FVariantArray& args)
{
	//GetEntity()
	KBEngine::Entity* e = GetEntity();
	if (e)
		e->BaseCall(name, args);
}

void UCS3EntityInterface::CellCallWithIntList(const FString &methodname, const TArray<int32> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::CellCallWithIntList(EntityID, methodname, arguments);
	}
}

void UCS3EntityInterface::CellCallWithFStringList(const FString &methodname, const TArray<FString> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::CellCallWithFStringList(EntityID, methodname, arguments);
	}
}

void UCS3EntityInterface::BaseCallWithBp(const FString &methodname, const TArray<FString> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::BaseCall(EntityID, methodname, arguments);
	}
}

void UCS3EntityInterface::BaseCall(const FString& name, KBEngine::FVariantArray& args)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3EntityInterface::pKBEApp!"));
		return;
	}
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3EntityInterface::BaseCall : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3EntityInterface::BaseCall : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	player->BaseCall(name, args);
}

void UCS3EntityInterface::BaseCallWithIntList(const FString &methodname, const TArray<int32> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::BaseCallWithIntList(EntityID, methodname, arguments);
	}
}

void UCS3EntityInterface::BaseCallWithFStringList(const FString &methodname, const TArray<FString> &arguments)
{
	if (EntityID != 0)
	{
		UGolbalBPFunctionLibrary::BaseCallWithFStringList(EntityID, methodname, arguments);
	}
}


UCS3EntityInterface* UCS3EntityInterface::GetInterfaceByName(FString interfacename)
{
	CS3Entity* tmp = static_cast<CS3Entity *>(GetEntity());
	if (!tmp)	//转换失败
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCS3EntityInterface::GetInterfaceByName : tmp!"));
		return nullptr;
	}
	return tmp->GetInterfaceByName(interfacename);
}


void UCS3EntityInterface::onEnterWorld()
{
	//CS3_Log(TEXT("UCS3EntityInterface::OnEnterWorld EntityId=[%d] ClassName=%s"), EntityID, *GetName());
	BP_onEnterWorld();
}

void UCS3EntityInterface::onLeaveWorld()
{
	//CS3_Log(TEXT("UCS3EntityInterface::OnLeaveWorld EntityId=[%d] ClassName=%s "), EntityID, *GetName());
	BP_onLeaveWorld();
}


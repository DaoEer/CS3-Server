// Fill out your copyright notice in the Description page of Project Settings.

#include "EntitySpaceEventInterface.h"
#include "KBEngine.h"
#include "Entity/Alias.h"
#include "GameData/SpaceEventType.h"
#include "Manager/MapManager.h"
#include "Chuangshi.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(UEntitySpaceEventInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UEntitySpaceEventInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

void UEntitySpaceEventInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
	ListenSpaceEvents.Empty();
}

void UEntitySpaceEventInterface::CLIENT_AddListenSpaceEvents_Implementation(const FString& SpaceScriptID, const int32& EventType, const int32& EventID, const FString& ConInfoStr)
{
	AddListenSpaceEvents_Implementation(SpaceScriptID, EventType, EventID, ConInfoStr);
}

void UEntitySpaceEventInterface::AddListenSpaceEvents_Implementation(const FString& SpaceScriptID, const int32& EventType, const int32& EventID, const FString& ConInfoStr)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("=====================Init space events===================="));
	FListenSpaceEvent pInst; 
	pInst.EventType = EventType;
	pInst.EventID = EventID;
	AliasSpaceEventConditions::CreateFromString(SpaceScriptID, EventType, EventID, ConInfoStr, pInst.ConsAlias);
	ListenSpaceEvents.Add(pInst);
}

void UEntitySpaceEventInterface::CLIENT_ClearListenSpaceEvents_Implementation()
{
	ClearListenSpaceEvents_Implementation();
}

void UEntitySpaceEventInterface::ClearListenSpaceEvents_Implementation()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("=====================Clear space events===================="));
	
	for (auto& Event : ListenSpaceEvents)
	{
		for (auto& info : Event.ConsAlias.Infos)
		{
			info->RemoveFromRoot();
		}
	}

	ListenSpaceEvents.Empty();
	UUECS3GameInstance::Instance->MapManager->ClearSpaceEventArea();
}

void UEntitySpaceEventInterface::onRoleChangeWorldArea(FString newArea, FString OldArea)
{
	if (!IsInListenSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_CHANGE_AREA)) return;
	TMap<FString, FString> Params;
	Params.Add(TEXT("oldArea"), OldArea);
	Params.Add(TEXT("newArea"), newArea);
	TriggerSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_CHANGE_AREA, Params);
}

void UEntitySpaceEventInterface::onRoleEnterEventArea(INT32 EventType, INT32 EventID)
{
	if (!IsInListenSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_ENTER_AREA)) return;
	TMap<FString, FString> Params;
	Params.Add(TEXT("eventType"), INT_TO_FSTRING(EventType));
	Params.Add(TEXT("eventID"), INT_TO_FSTRING(EventID));
	TriggerSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_ENTER_AREA, Params);
}

void UEntitySpaceEventInterface::onRoleLeaveEventArea(int32 EventType, int32 EventID)
{
	if (!IsInListenSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_LEAVE_AREA)) return;
	TMap<FString, FString> Params;
	Params.Add(TEXT("eventType"), INT_TO_FSTRING(EventType));
	Params.Add(TEXT("eventID"), INT_TO_FSTRING(EventID));
	TriggerSpaceEvent(SPACE_EVENT_TYPE::SPACE_EVENT_TYPE_ROLE_LEAVE_AREA, Params);
}

bool UEntitySpaceEventInterface::IsInListenSpaceEvent(int32 EventType)
{
	for (auto& fEvent : ListenSpaceEvents)
	{
		if (fEvent.EventType == EventType)
		{
			return true;
		}
	}
	return false;
}

void UEntitySpaceEventInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_AddListenSpaceEvents");
	ArrBlueFunc.Add("CLIENT_ClearListenSpaceEvents");
	ArrBlueFunc.Add("CLIENT_SpaceEventPlayAction");
	Supper::InitBlueCB();
}

void UEntitySpaceEventInterface::CLIENT_SpaceEventPlayAction_Implementation(const TArray<FString>& AtionIDs)
{
	SpaceEventPlayAction_Implementation(AtionIDs);
}

void UEntitySpaceEventInterface::SpaceEventPlayAction_Implementation(const TArray<FString>& AtionIDs)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::spaceEventPlayAction_Implementation : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("=====================play actions====================%d"),GetEntity()->ID());
}

bool UEntitySpaceEventInterface::CheckEventConditions(AliasSpaceEventConditions& ConsAlias, const TMap<FString, FString> & Params)
{
	for (auto Con : ConsAlias.Infos)
	{
		if (!Con->CheckCondition(GetEntity(), Params))
			return false;
	}
	return true;
}

void UEntitySpaceEventInterface::TriggerSpaceEvent(int32 EventType, const TMap<FString, FString> & Params)
{

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEntitySpaceEventInterface::TriggerSpaceEvent : GetEntity()!"));
		return;
	}
	TArray<int32> tEventIDs;
	for(auto fEvent : ListenSpaceEvents) 
	{
		if (fEvent.EventType != EventType)
			continue;
		
		if (!CheckEventConditions(fEvent.ConsAlias, Params))
			continue;
		
		tEventIDs.Add(fEvent.EventID);
	}
	RPC_TriggerSpaceEventByClient(EventType, tEventIDs, MapToString(Params));
}

FString UEntitySpaceEventInterface::MapToString(TMap<FString, FString> tMap)
{
	FString MapStr_ = "";

	for (auto it = tMap.CreateIterator(); it; ++it)
	{
		MapStr_ += FString::Printf(TEXT("\"%s\": \"%s\","), *(it.Key()), *(it.Value()));
	}
	MapStr_ = FString::Printf(TEXT("{%s}"), *MapStr_);
	return MapStr_;
}

void UEntitySpaceEventInterface::RPC_TriggerSpaceEventByClient(int32 EventType, TArray<int32> tEventIDs, FString Params)
{
	KBEngine::Entity* Entity = GetEntity();
	if (!Entity)
	{
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(EventType);
	Args.Add(KBEngine::FVariantArray(tEventIDs));
	Args.Add(Params);

	Entity->CellCall(TEXT("CELL_triggerSpaceEventByClient"), Args);
}
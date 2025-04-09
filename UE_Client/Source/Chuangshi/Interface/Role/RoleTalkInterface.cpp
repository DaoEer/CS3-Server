// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleTalkInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../SpellBox/SpellBoxInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "KBEngine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/GameObject.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTalkInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTalkInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleTalkInterface::URoleTalkInterface()
{
}

URoleTalkInterface::~URoleTalkInterface()
{
}

void URoleTalkInterface::RefreshAroundBoxStatus_Implementation(int32 eventType)
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTalkInterface::RefreshAroundBoxStatus_Implementation : GetActor()!"));
		return;
	}
	if (GetEntity()==nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTalkInterface::RefreshAroundBoxStatus_Implementation : GetEntity()!"));
		return;
	}
	KBEngine::KBEngineApp* KbeApp = UUECS3GameInstance::pKBEApp;
	if (KbeApp==nullptr || KbeApp->Entities()==nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTalkInterface::RefreshAroundBoxStatus_Implementation : KbeApp!"));
		return;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *KbeApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* _Entity = Elem.Value;
		if (!_Entity)continue;
		USpellBoxInterface * Interface = Cast<USpellBoxInterface>(((GameObject*)_Entity)->Interface_Cache.GameObjectInterface);
		if (IsValid(Interface))
		{
			if (!Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_SPELL))continue;
			if (Interface->HasListenEvent(eventType))
			{
				Interface->CLIENT_RefreshBoxStatus();
			}
		}
	}
}

void URoleTalkInterface::OnChangeTalkState(bool IsTalking)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter))
	{
		PlayerCharacter->SetRoleInteractive(IsTalking);
		if (IsTalking)
		{
			PlayerCharacter->StopRandomAction();
		}
	}
}

void URoleTalkInterface::openStoreWindown_Implementation(const int32& npcID)
{
}

void URoleTalkInterface::RPC_talkWithMonster(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTalkInterface::RPC_talkWithMonster : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("talkWithMonster"), args);
}

void URoleTalkInterface::CELL_RequestRefreshAreaStatus(int32 entityID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTalkInterface::CELL_RequestRefreshAreaStatus : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(entityID);
	entity->CellCall(TEXT("CELL_RequestRefreshAreaStatus"), args);
}

void URoleTalkInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onSetGossipText");
	ArrBlueFunc.Add("onAddGossipOption");
	ArrBlueFunc.Add("onGossipComplete");
	ArrBlueFunc.Add("RefreshAroundBoxStatus");
	ArrBlueFunc.Add("onPlayGossipVoice");
	ArrBlueFunc.Add("onSetMonsterGossipText");
	ArrBlueFunc.Add("onAddMonsterGossipOption");
	ArrBlueFunc.Add("onMonsterGossipComplete");
	Supper::InitBlueCB();
}

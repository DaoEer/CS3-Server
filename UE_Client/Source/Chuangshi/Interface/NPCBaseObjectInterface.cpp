// Fill out your copyright notice in the Description page of Project Settings.

#include "NPCBaseObjectInterface.h"

#include "GameData/GameDefault.h"

#include "GameDevelop/CS3GameInstance.h"
#include "Actor/ServerCharacter.h"
#include "CS3Base/GameObject.h"
#include "Entity/NPCBaseObject.h"
#include "WidgetComponent.h"
#include "Manager/ParticleManager.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"
#include "Manager/CustomTimerManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCBaseObjectInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCBaseObjectInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(uname, &UNPCBaseObjectInterface::Set_UName, FString)
CS3_END_INTERFACE_PROPERTY_MAP()

UNPCBaseObjectInterface::UNPCBaseObjectInterface()
{
}

UNPCBaseObjectInterface::~UNPCBaseObjectInterface()
{
}

void UNPCBaseObjectInterface::OnRep_modelNumber()
{
}


void UNPCBaseObjectInterface::OnRep_SyncPosClient()
{
	NPCBaseObject* entity = (NPCBaseObject*)GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCBaseObjectInterface::OnRep_SyncPosClient : entity!"));
		return;
	}
	int32 newValue = entity->GetDefinedProperty(TEXT("SyncPosClient")).GetValue<int32>();
	if (newValue == old_SyncPosClient)return;
	entity->SetSyncPosClient(newValue, old_SyncPosClient);
}

void UNPCBaseObjectInterface::PlayBeforeSpawnEffect(AServerCharacter* actor)
{
	if (!IsValid(actor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCBaseObjectInterface::PlayBeforeSpawnEffect : actor!"));
		return;
	}

	//播放出生前光效
 	GameObject* entity = (GameObject*)actor->GetSelfEntity();
	if (entity != nullptr && IsValid(UUECS3GameInstance::Instance))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		FString ScriptID = (FString)(entity->GetDefinedProperty(TEXT("scriptID")));
		if (entity->GetActorName() == TEXT("Monster"))
		{
			const FMONSTER_DATA* MonsterData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MONSTER)->GetRow<FMONSTER_DATA>(ScriptID);
			if (MonsterData && !MonsterData->BeforeSpawnEffectId.IsEmpty())
			{
				UUECS3GameInstance::Instance->ParticleManager->PlayParticle(MonsterData->BeforeSpawnEffectId, 0.0f, actor, actor);

				TWeakObjectPtr<UNPCBaseObjectInterface> DelayThisPtr(this);
				TWeakObjectPtr<AServerCharacter> DelayActorPtr(actor);
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, EffectTimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, DelayActorPtr]()
					{
						if (DelayThisPtr.IsValid() && DelayActorPtr.IsValid())
						{
							UNPCBaseObjectInterface* ThisPtr = DelayThisPtr.Get();
							AServerCharacter* ActorPtr = DelayActorPtr.Get();
							ThisPtr->ShowAndUpdataActor(ActorPtr);
						}
					}), 0.1f, false, MonsterData->BeforeSpawnPlayEffectTime);
				}
			}
			else
			{
				ShowAndUpdataActor(actor);
			}
		}
		else if (entity->GetActorName() == TEXT("NPC"))
		{
			const FNPC_DATA* NPCData = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC)->GetRow<FNPC_DATA>(ScriptID);
			if (NPCData && !NPCData->BeforeSpawnEffectId.IsEmpty())
			{
				UUECS3GameInstance::Instance->ParticleManager->PlayParticle(NPCData->BeforeSpawnEffectId, 0.0f, actor, actor);

				TWeakObjectPtr<UNPCBaseObjectInterface> DelayThisPtr(this);
				TWeakObjectPtr<AServerCharacter> DelayActorPtr(actor);
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, EffectTimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, DelayActorPtr]()
					{
						if (DelayThisPtr.IsValid() && DelayActorPtr.IsValid())
						{
							UNPCBaseObjectInterface* ThisPtr = DelayThisPtr.Get();
							AServerCharacter* ActorPtr = DelayActorPtr.Get();
							ThisPtr->ShowAndUpdataActor(ActorPtr);
						}
					}), 0.1f, false, NPCData->BeforeSpawnPlayEffectTime);
				}
			}
			else
			{
				ShowAndUpdataActor(actor);
			}
		}
		else
		{
			ShowAndUpdataActor(actor);
		}
	}
}

void UNPCBaseObjectInterface::ShowAndUpdataActor(AServerCharacter* actor)
{
	UGolbalBPFunctionLibrary::SetActorAndCompVisibility(actor, UPrimitiveComponent::StaticClass());
	if (KBEngine::Entity* entity = actor->GetSelfEntity())
	{
		actor->CreateAppearance();
	}
	actor->SetInitialized(true);
	actor->OnActorCreateFinish.Broadcast();
}

void UNPCBaseObjectInterface::onEnterWorld()
{
	Supper::onEnterWorld();
}

void UNPCBaseObjectInterface::onLeaveWorld()
{	
	if (EffectTimerHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
		}
	}
	Supper::onLeaveWorld();
}

void UNPCBaseObjectInterface::RPC_CELL_gossipWith()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCInterface::RPC_CELL_gossipWith : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_gossipWith"), args);
}


void UNPCBaseObjectInterface::Set_UName(const FString& newVal, const FString& oldVal)
{
	uname = newVal;
}
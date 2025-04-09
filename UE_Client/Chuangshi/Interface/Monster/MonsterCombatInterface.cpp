// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterCombatInterface.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Manager/ParticleManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomCursorManager.h"
#include "Engine/EngineTypes.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterCombatInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OpenMoveShield, &UMonsterCombatInterface::OpenMoveShield, const int32&, const FString&, float, float, const FString&, float, float)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CloseMoveShield, &UMonsterCombatInterface::CloseMoveShield, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &UMonsterCombatInterface::Set_HP, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP_Max, &UMonsterCombatInterface::Set_HP_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(camp, &UMonsterCombatInterface::Set_camp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue, &UMonsterCombatInterface::Set_gangQiValue, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue_Max, &UMonsterCombatInterface::Set_gangQiValue_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiState, &UMonsterCombatInterface::Set_gangQiState, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(tempCamp, &UMonsterCombatInterface::Set_tempCamp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQi_qiJieProgress, &UMonsterCombatInterface::Set_gangQi_qiJieProgress, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(title, &UMonsterCombatInterface::Set_title, FString )
CS3_END_INTERFACE_PROPERTY_MAP()


void UMonsterCombatInterface::Set_HP(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnHPChanged(HP, HP_Max);
		}

	}

}

void UMonsterCombatInterface::Set_HP_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP_Max(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnHPChanged(HP, HP_Max);
		}

	}
}


void UMonsterCombatInterface::Set_camp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_camp(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnCampChanged( camp );
		}
		
	}
}

void UMonsterCombatInterface::Set_gangQiValue(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnGangQiChanged( gangQiValue, gangQiValue_Max );
		}

	}
}

void UMonsterCombatInterface::Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue_Max(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnGangQiChanged(gangQiValue, gangQiValue_Max);
		}

	}
}

void UMonsterCombatInterface::Set_gangQiState(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiState(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnGangQiStateChanged(gangQiState);
		}

	}
}

void UMonsterCombatInterface::Set_tempCamp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_tempCamp(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnTempCampChanged(tempCamp);
		}

	}
}

void UMonsterCombatInterface::Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQi_qiJieProgress(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		AMonsterCharacter* mActorPtr = Cast< AMonsterCharacter >(actorPtr);
		if (IsValid(mActorPtr))
		{
			mActorPtr->OnGangQiProgressChanged(gangQi_qiJieProgress, gangQiValue_Max);
		}

	}
}

void UMonsterCombatInterface::Set_title(const FString& newVal, const FString& oldVal)
{
	titleStr = newVal;
}

void UMonsterCombatInterface::OpenMoveShield(const int32& ID, const FString& Effect1, float IntervalTime1, float Angel1, const FString& Effect2, float IntervalTime2, float Angel2)
{
	PlayShieldParticle(Effect1, 1, IntervalTime1, Angel1);
	PlayShieldParticle(Effect2, 2, IntervalTime2, Angel2);
	//OpenMoveShield_BP(ID, Position);//废弃，换新的粒子表现
}


void UMonsterCombatInterface::PlayShieldParticle(const FString& EffectId, int32 index, float IntervalTime, float Angel)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(GetActor());
	if (MonsterCharacter)
	{
		TWeakObjectPtr<AMonsterCharacter> ActorPtr(MonsterCharacter);
		UParticleManager* ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
		TWeakObjectPtr<UMonsterCombatInterface> DelayThisPtr(this);
		int32 EffectUID = ParticleManager->PlayParticle(EffectId, 0.0f, MonsterCharacter, MonsterCharacter, FEffectCreate::CreateLambda([ActorPtr, DelayThisPtr, index, IntervalTime, Angel](int32 UID)
		{
			AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
			if (IsValid(Effect) && ActorPtr.IsValid() && DelayThisPtr.IsValid())
			{
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UMonsterCombatInterface* MonsterCombatInterface = DelayThisPtr.Get();
					if (IsValid(MonsterCombatInterface))
					{
						int32 t;
						if (index == 1)
						{
							MonsterCombatInterface->EffectUId1 = UID;
							t = 1;
						}
						else
						{
							MonsterCombatInterface->EffectUId2 = UID;
							t = -1;
						}
						FTimerHandle TimerHandle;
						TWeakObjectPtr<AActor> EffectPtr(Effect);
						UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(Effect, TimerHandle,
							FTimerDelegate::CreateLambda([EffectPtr, t, Angel]()
						{
							if (EffectPtr.IsValid())
							{
								AActor* Effect = EffectPtr.Get();
								FRotator Rotation = Effect->GetActorRotation();
								Rotation.Yaw += t * Angel;
								Effect->SetActorRotation(Rotation);
							}
						}), IntervalTime, true);
					}
				}
			}
		}));
	}
}

void UMonsterCombatInterface::CloseMoveShield(const int32& ID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ParticleManager))
	{
		AActor* Effect1 = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(EffectUId1);
		if (IsValid(Effect1))
		{
			UUECS3GameInstance::Instance->ClearObjectHandles(Effect1);
			UUECS3GameInstance::Instance->ParticleManager->Stop(Cast<AEffectEmitter>(Effect1));
		}
		AActor* Effect2 = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(EffectUId2);
		if (IsValid(Effect2))
		{
			UUECS3GameInstance::Instance->ClearObjectHandles(Effect2);
			UUECS3GameInstance::Instance->ParticleManager->Stop(Cast<AEffectEmitter>(Effect2));
		}
		
	}
	//CloseMoveShield_BP(ID);
}

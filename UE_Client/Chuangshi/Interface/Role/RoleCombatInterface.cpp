// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleCombatInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Pet/PetCharacter.h"
#include "Interface/Role/RolePetInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/GlobalFunctions.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCombatInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(camp, &URoleCombatInterface::Set_camp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP, &URoleCombatInterface::Set_HP, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(HP_Max, &URoleCombatInterface::Set_HP_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue, &URoleCombatInterface::Set_gangQiValue, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiValue_Max, &URoleCombatInterface::Set_gangQiValue_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQiState, &URoleCombatInterface::Set_gangQiState, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(title, &URoleCombatInterface::Set_title, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(tempCamp, &URoleCombatInterface::Set_tempCamp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQi_qiJieProgress, &URoleCombatInterface::Set_gangQi_qiJieProgress, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(killingValue, &URoleCombatInterface::Set_killingValue, int32)
CS3_END_INTERFACE_PROPERTY_MAP()


void URoleCombatInterface::Set_HP(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnHPChanged(HP, HP_Max);
		}
	}
	
}

void URoleCombatInterface::Set_HP_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_HP_Max(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnHPChanged(HP, HP_Max);
		}

	}
}

void URoleCombatInterface::Set_camp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_camp(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnCampChanged(camp);
		}

	}
}

void URoleCombatInterface::Set_gangQiValue(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnGangQiChanged(gangQiValue, gangQiValue_Max);
		}

	}
}

void URoleCombatInterface::Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiValue_Max(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnGangQiChanged(gangQiValue, gangQiValue_Max);
		}

	}
}

void URoleCombatInterface::Set_gangQiState(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQiState(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnGangQiStateChanged(gangQiState);
		}

	}
}

void URoleCombatInterface::Set_title(const int32& newVal, const int32& oldVal)
{
	title = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnTitleChanged.Broadcast( EntityID,  title );
	}

	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnTitleChanged();
		}
	}
}

void URoleCombatInterface::Set_tempCamp(const int32& newVal, const int32& oldVal)
{
	Supper::Set_tempCamp(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnTempCampChanged( tempCamp );
		}
	}
}

void URoleCombatInterface::Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)
{
	Supper::Set_gangQi_qiJieProgress(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnGangQiProgressChanged(gangQi_qiJieProgress, gangQiValue_Max);
		}
	}
}

void URoleCombatInterface::Set_killingValue(const int32& newVal, const int32& oldVal)
{
	Supper::Set_killingValue(newVal, oldVal);
	AActor* actorPtr = GetActor();
	if (IsValid(actorPtr))
	{
		APlayerCharacter* pActorPtr = Cast< APlayerCharacter >(actorPtr);
		if (IsValid(pActorPtr))
		{
			pActorPtr->OnKillingValueChanged();
		}
	}
	URolePetInterface* petIntPtr = CS3::GetInterface< URolePetInterface >(EntityID);
	if (petIntPtr->petEntityID != 0)
	{
		AActor* actorPtr2 = UGolbalBPFunctionLibrary::GetActorByID(petIntPtr->petEntityID);
		if (IsValid(actorPtr2))
		{
			APetCharacter* petAcotrPtr = Cast< APetCharacter >(actorPtr2);
			if (IsValid(petAcotrPtr))
				petAcotrPtr->OnKillingValueChanged();
		}
	}

}
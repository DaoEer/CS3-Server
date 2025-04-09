// Fill out your copyright notice in the Description page of Project Settings.

#include "CustomTimerManager.h"
#include "Engine/GameInstance.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include"Chuangshi.h"
#include "Entity.h"
#include "UObject/UObjectHash.h"
#include "UObject/UObjectBase.h"

CONTROL_COMPILE_OPTIMIZE_START

UCustomTimerManager* UCustomTimerManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UCustomTimerManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_CustomTimerManager")));
}

void UCustomTimerManager::AddItemToMap(const FString& ClassName, FTimerStruct& Timer)
{
	UpdateMap();

	if (TimerMap.Contains(ClassName))
	{
		TimerMap[ClassName].Add(Timer);
	}
	else
	{
		TArray<FTimerStruct> HandleList;
		HandleList.Add(Timer);
		TimerMap.Add(ClassName, HandleList);
	}
}

void UCustomTimerManager::AddToMap(FTimerStruct& Timer, void* InObj)
{
	if (!InObj)
	{
		AddItemToMap("UnKnown", Timer);
		return;
	}

	// 检测UObject的有效性
	UObjectBase* CuurrentObject = (UObjectBase*)(InObj);
	int32 Index = GUObjectArray.ObjectToIndex(CuurrentObject);
	if (GUObjectArray.IsValidIndex(CuurrentObject))
	{
		// 判断一下找到的东西地址是否一致
		if (CuurrentObject == GUObjectArray.IndexToObject(Index)->Object)
		{
			AddItemToMap(CuurrentObject->GetClass()->GetName(), Timer);
			return;
		}
	}

	KBEngine::Entity* CurrentEntity = (KBEngine::Entity*)(InObj);
	int32 ID = CurrentEntity->ID();
	if (UGolbalBPFunctionLibrary::FindEntity(ID))
	{
		// 判断一下找到的东西地址是否一致
		if (CurrentEntity == UGolbalBPFunctionLibrary::FindEntity(ID))
		{
			AddItemToMap(CurrentEntity->ClassName(), Timer);
			return;
		}
	}
	
	AddItemToMap("UnKnown", Timer);
}

void UCustomTimerManager::UpdateMap()
{
	UGameInstance* Instance = UUECS3GameInstance::Instance;

	// 遍历删除没用的定时器
	for (auto it1 = TimerMap.CreateIterator(); it1; ++it1)
	{
		for (auto it2 = it1->Value.CreateIterator(); it2; ++it2)
		{
			if (!Instance->GetTimerManager().TimerExists(it2->Handle))
			{
				it2.RemoveCurrent();
			}
		}

		if (!it1->Value.Num())
		{
			it1.RemoveCurrent();
		}
	}
}

int32 UCustomTimerManager::GetTimerNumberByClassName(const FString& InClassName)
{
	if (TimerMap.Contains(InClassName))
	{
		UpdateMap();
		return TimerMap[InClassName].Num();
	}
	else
	{
		return 0;
	}
}

TMap<FString, int32> UCustomTimerManager::GetTimerMap()
{
	UpdateMap();
	
	TMap<FString, int32> CurrentTimerMap;
	for (auto& Timer : TimerMap)
	{
		CurrentTimerMap.Add(Timer.Key, Timer.Value.Num());
	}
	return CurrentTimerMap;
}

void UCustomTimerManager::ClearAllTimer()
{
	UpdateMap();
	for (auto& Timer : TimerMap)
	{
		for (auto& Handle : Timer.Value)
		{
			ClearTimer(Handle.Handle);
		}
	}
	UpdateMap();
}

void UCustomTimerManager::ClearTimer(FTimerHandle& InHandle)
{
	GetTimerManager().ClearTimer(InHandle);
}

void UCustomTimerManager::ClearAllTimersForObject(void const* Object)
{
	if (!IsValid(this))
	{
		// shutdown后还有多地方在使用UCustomTimerManager
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UCustomTimerManager is NULL"));
		return;
	}

	for (auto& Timer : TimerMap)
	{
		for (auto& Handle : Timer.Value)
		{
			if (Handle.Object == Object)
			{
				ClearTimer(Handle.Handle);
			}
		}
	}

	UpdateMap();
}

void UCustomTimerManager::PauseTimer(FTimerHandle InHandle)
{
	GetTimerManager().PauseTimer(InHandle);
}

void UCustomTimerManager::UnPauseTimer(FTimerHandle InHandle)
{
	GetTimerManager().UnPauseTimer(InHandle);
}

bool UCustomTimerManager::IsTimerActive(FTimerHandle InHandle) const
{
	return GetTimerManager().IsTimerActive(InHandle);
}

bool UCustomTimerManager::IsTimerPaused(FTimerHandle InHandle)
{
	return GetTimerManager().IsTimerPaused(InHandle);
}

bool UCustomTimerManager::IsTimerPending(FTimerHandle InHandle)
{
	return GetTimerManager().IsTimerPending(InHandle);
}

bool UCustomTimerManager::TimerExists(FTimerHandle InHandle)
{
	return GetTimerManager().TimerExists(InHandle);
}

float UCustomTimerManager::GetTimerRemaining(FTimerHandle InHandle) const
{
	return GetTimerManager().GetTimerRemaining(InHandle);
}

FTimerManager& UCustomTimerManager::GetTimerManager() const
{
	UGameInstance* Instance = Cast<UGameInstance>(UUECS3GameInstance::Instance);
	return Instance->GetTimerManager();
}

CONTROL_COMPILE_OPTIMIZE_END


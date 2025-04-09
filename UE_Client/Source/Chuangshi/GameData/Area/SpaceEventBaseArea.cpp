// Fill out your copyright notice in the Description page of Project Settings.

#include "SpaceEventBaseArea.h"
#include "Vector.h"
#include "Actor/ServerCharacter.h"
#include "Interface/EntitySpaceEventInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "CS3Base/GameObject.h"


USpaceEventBaseArea::USpaceEventBaseArea()
{
}

USpaceEventBaseArea::~USpaceEventBaseArea()
{

}

void USpaceEventBaseArea::InitParams(FString _ScriptID, INT32 _EventType, INT32 _EventID, FString Param1, FString Param2, FString Param3)
{
	EventType = _EventType;
	EventID = _EventID;
	ScriptID = _ScriptID;
	MapScriptID = _ScriptID;
}

void USpaceEventBaseArea::OnEnter(const FString SpaceScriptID)
{
	UEntitySpaceEventInterface* EntitySpaceEventInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.EntitySpaceEventInterface : nullptr;
	if (EntitySpaceEventInterface)
	{
		EntitySpaceEventInterface->onRoleEnterEventArea(EventType, EventID);
	}
}

void USpaceEventBaseArea::OnLeave(const FString SpaceScriptID)
{
	UEntitySpaceEventInterface* EntitySpaceEventInterface = UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.EntitySpaceEventInterface : nullptr;
	if (EntitySpaceEventInterface)
	{
		EntitySpaceEventInterface->onRoleLeaveEventArea(EventType, EventID);
	}
}

bool USpaceEventBaseArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceEventBaseArea::IsPlayerIn : PlayerActor!"));
		return false;
	}

	FVector PlayerPosition = PlayerActor->GetActorLocation();
	return IsPointIn(PlayerPosition);

}
// Fill out your copyright notice in the Description page of Project Settings.


#include "TickObject.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"


UTickObject::UTickObject()
	:Super()
{
	CustomTimeDilation = 1.0;
	SumDeltaTime = 0.0f;
	SumTickTime = 0.0f;
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Create A TickObject[%d]"), GetUniqueID());
}

void UTickObject::PostInitProperties()
{
	Super::PostInitProperties();
	if (bCanEverTick)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("TickObject[%d] start tick function!"), GetUniqueID());
	}
	if (CustomTimeDilation < 0.1)
	{
		CS3_Warning(TEXT("TickObject[%d] set tick DeltaTime[%f]"), GetUniqueID(), CustomTimeDilation);
	}
}

void UTickObject::BeginDestroy()
{
	Super::BeginDestroy();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("BeginDestroy A TickObject[%d]"), GetUniqueID());
}

UTickObject::~UTickObject()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Create A TickObject[%d]"), GetUniqueID());
}

void UTickObject::Tick(float DeltaTime)
{
	if (!bCanEverTick)	return;
	SumDeltaTime += DeltaTime;
	SumTickTime += DeltaTime;
	if (SumDeltaTime >= CustomTimeDilation)
	{
		TickObject();
		SumDeltaTime = 0.0;
	}
}

bool UTickObject::IsPlaying()
{
	if (UUECS3GameInstance::Instance)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UTickObject::IsInWorld()
{
	if ((UUECS3GameInstance::Instance) && (UUECS3GameInstance::Instance->pKBEApp) && (UUECS3GameInstance::Instance->pKBEApp->Player()))
	{
		return true;
	}
	else
	{
		return false;
	}
}
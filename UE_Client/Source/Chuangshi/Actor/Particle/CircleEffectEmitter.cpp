// Fill out your copyright notice in the Description page of Project Settings.


#include "CircleEffectEmitter.h"
#include "GameData/EffectEmitterData.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"

ACircleEffectEmitter::ACircleEffectEmitter()
{
	PrimaryActorTick.bCanEverTick = false;
	PrimaryActorTick.bStartWithTickEnabled = false;
}

void ACircleEffectEmitter::InitFromConfig()
{
	AEffectEmitter::InitFromConfig();
	const FCIRCLE_DATA CircleEffectData = EffectEmitterData->EffectData.CircleEffectData;
	SetCircleEffectParameter(CircleEffectData.IsMove, CircleEffectData.StartSpawnNum, CircleEffectData.StartRadius, CircleEffectData.TotalTime, CircleEffectData.IntervalTime);
}

void ACircleEffectEmitter::SetCircleEffectParameter(bool InIsMove, float InStartSpawnNum, float InStartRadius, float InTotalTime, float InIntervalTime)
{
	StartSpawnNum = InStartSpawnNum;
	StartRadius = InStartRadius;
	Radius = InStartRadius;
	TotalTime = InTotalTime;
	IntervalTime = InIntervalTime;
	SetFloatParameter("NUM", InStartSpawnNum);
	SetFloatParameter("Speed", InStartRadius);
	if (InIsMove)
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UCustomTimerManager* CustomTimerManager = UUECS3GameInstance::Instance->CustomTimerManager;
			if (IsValid(CustomTimerManager))
			{
				CustomTimerManager->SetTimer(timerHandle, this,
					&ACircleEffectEmitter::Move, IntervalTime, true);
			}
		}
	}
}

void ACircleEffectEmitter::Move()
{
	if (Radius<= 1.e-6f)
	{
		StopMove();
	}
	else
	{
		Radius -= (StartRadius / TotalTime) * IntervalTime;
		float SpawnNum;
		SpawnNum = (Radius / StartRadius) * StartSpawnNum;
		SetFloatParameter("NUM", SpawnNum);
		SetFloatParameter("Speed", Radius);
	}
}

void ACircleEffectEmitter::StopMove()
{
	Radius = 0;
	SetFloatParameter("NUM", 0);
	SetFloatParameter("Speed", 0);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UCustomTimerManager* CustomTimerManager = UUECS3GameInstance::Instance->CustomTimerManager;
		if (IsValid(CustomTimerManager))
		{
			CustomTimerManager->ClearTimer(timerHandle);
		}
	}
}

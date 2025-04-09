// Fill out your copyright notice in the Description page of Project Settings.


#include "ParabolaEffectEmitter.h"
#include "Util\ConvertUtil.h"


CONTROL_COMPILE_OPTIMIZE_START

void AParabolaEffectEmitter::InitEmitterTransform()
{
	AFlyEffectEmitter::InitEmitterTransform();
	if (EffectData->FlyData.FlyTime == 0.0f && EffectData->FlyData.FlySpeed == 0.0f)return;

	GravityZ = -980.0f;
	FVector SrcPos = GetFlySourcePos();
	FVector DstPos = GetFlyTargetPos();

	// 使用飞行速度
	float FlyTime = EffectData->FlyData.FlyTime;
	if (!EffectData->FlyData.bIsFlyByTime ||  FlyTime == 0.0f)
	{
		FlyTime = (DstPos - SrcPos).Size2D() / EffectData->FlyData.FlySpeed;
	}
	if (!EffectData->FlyData.FlyGravityZ.IsEmpty())
	{
		GravityZ = FSTRING_TO_FLOAT(EffectData->FlyData.FlyGravityZ);
	}

	_FlySpeed = (DstPos - SrcPos) / FlyTime;
	_FlySpeed.Z = (DstPos.Z - SrcPos.Z - 0.5 * GravityZ * FMath::Square(FlyTime)) / FlyTime;
	float SpeedZ = EffectData->FlyData.FlySpeed;
	
}

void AParabolaEffectEmitter::Tick(float DeltaTime)
{
	float TargetDist = (TargetPos - GetActorLocation()).Size();
	if (TargetDist <= 1.0f)
	{
		SetActorLocation(TargetPos);
		OnEffectArrived.Broadcast();
		Stop();//结束移动
		return;
	}

	FVector Gravity(0.0, 0.0, GravityZ);
	FVector deltaDist = _FlySpeed * DeltaTime + Gravity / 2 * FMath::Square(DeltaTime);
	if (TargetDist <= deltaDist.Size())
	{
		SetActorLocation(TargetPos);
		OnEffectArrived.Broadcast();
		Stop();//结束移动
		return;
	}

	SetActorLocation(GetActorLocation() + deltaDist);
	_FlySpeed += Gravity * DeltaTime;
}

CONTROL_COMPILE_OPTIMIZE_END
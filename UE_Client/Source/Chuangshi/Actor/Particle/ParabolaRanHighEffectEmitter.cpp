// Fill out your copyright notice in the Description page of Project Settings.


#include "ParabolaRanHighEffectEmitter.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"

void AParabolaRanHighEffectEmitter::InitEmitterTransform()
{
	AParabolaEffectEmitter::InitEmitterTransform();

	GravityZ = -980.0f;
	FVector SrcPos = GetFlySourcePos();
	FVector DstPos = GetFlyTargetPos();
	if (!EffectData->FlyData.FlyGravityZ.IsEmpty())
	{
		GravityZ = FSTRING_TO_FLOAT(EffectData->FlyData.FlyGravityZ);
	}

	TArray<FString> RandomHighs = UGolbalBPFunctionLibrary::SplitString(EffectData->FlyData.FlyMaxHighRan);
	float MaxHight(0.0);
	if (RandomHighs.Num() >= 2)
	{
		MaxHight = FMath::RandRange(FSTRING_TO_FLOAT(RandomHighs[0]), FSTRING_TO_FLOAT(RandomHighs[1]));
	}
	else if (RandomHighs.Num())
	{
		MaxHight = FSTRING_TO_FLOAT(RandomHighs[0]);
	}

	float SpeedZ = FMath::Sqrt(-2 * MaxHight / GravityZ)*-GravityZ;
	float Time = FMath::Sqrt(2 * (DstPos.Z - SrcPos.Z) / GravityZ + FMath::Square(SpeedZ / GravityZ)) - SpeedZ / GravityZ;

	_FlySpeed = (DstPos - SrcPos) / Time;
	_FlySpeed.Z = SpeedZ;
	
}

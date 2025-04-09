// Fill out your copyright notice in the Description page of Project Settings.


#include "ShelterEffectEmitter.h"
#include "Particles/ParticleSystemComponent.h"
#include "GameFramework/Character.h"
#include "Util/GolbalBPFunctionLibrary.h"

void AShelterEffectEmitter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
}

void AShelterEffectEmitter::StartPlay()
{
	ShelterRadius = EffectEmitterData->EffectData.ShelterData.ShelterRadius;
	ShelterBoundID = EffectEmitterData->EffectData.ShelterData.ShelterEffectID;
	ShelterIsBound = EffectEmitterData->EffectData.ShelterData.IsBind;
	ShelterLoc = EffectEmitterData->EffectData.ShelterData.ShelterPosition;
// 	Sceondtarget = Cast<ACharacter>(SecondTarget);
// 	if (!IsValid(Sceondtarget))
// 	{
// 		Sceondtarget = Cast<ACharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
// 	}
	if (!EffectEmitterData->EffectData.ShelterData.IsBind)
	{
		this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereX"), EffectEmitterData->EffectData.ShelterData.ShelterPosition.X);
		this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereY"), EffectEmitterData->EffectData.ShelterData.ShelterPosition.Y);
		this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereZ"), EffectEmitterData->EffectData.ShelterData.ShelterPosition.Z);
		this->GetParticleSystemComponent()->SetFloatParameter(TEXT("Radius"), EffectEmitterData->EffectData.ShelterData.ShelterRadius * 10);
 	}
	TArray<AActor*> effectList;
	UGolbalBPFunctionLibrary::GetAllActorsOfClassExt(AEffectEmitter::StaticClass(), effectList);
	for (AActor* actor : effectList)
	{
		AEffectEmitter* effectEmitter = Cast<AEffectEmitter>(actor);
		if (IsValid(effectEmitter))
		{
			if (ShelterBoundID.Equals(effectEmitter->GetEffectID()))
			{
				ShelterEmitter = effectEmitter;
			}
		}
	}
 	this->GetParticleSystemComponent()->ActivateSystem(true);
	Super::StartPlay();
}

void AShelterEffectEmitter::Tick(float DeltaSeconds)
{
		if (IsValid(ShelterEmitter) && EffectEmitterData->EffectData.ShelterData.IsBind)
		{
			this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereX"), ShelterEmitter->GetActorLocation().X);
			this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereY"), ShelterEmitter->GetActorLocation().Y);
			this->GetParticleSystemComponent()->SetFloatParameter(TEXT("SphereZ"), ShelterEmitter->GetActorLocation().Z );
			this->GetParticleSystemComponent()->SetFloatParameter(TEXT("Radius"), EffectEmitterData->EffectData.ShelterData.ShelterRadius * 10);
 	}
	Super::Tick(DeltaSeconds);
}

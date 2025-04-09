// Fill out your copyright notice in the Description page of Project Settings.

#include "SequencerEmitter.h"
#include "Particles/ParticleSystemComponent.h"


void ASequencerEmitter::SetWarmupTime(float Value)
{
	while (DeltaTime < Value)
	{
		GetParticleSystemComponent()->TickComponent(0.032f, LEVELTICK_All, NULL);
		DeltaTime += 0.032f;
	}
	DeltaTime = 0.f;
}


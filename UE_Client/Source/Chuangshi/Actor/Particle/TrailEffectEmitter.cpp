// Fill out your copyright notice in the Description page of Project Settings.

#include "TrailEffectEmitter.h"
// UE4
#include "GameFramework/Character.h"
#include "Particles/ParticleSystemComponent.h"
#include "Components/SkeletalMeshComponent.h"
// 数据类型
#include "Util/CS3Debug.h"
#include "GameData/EffectEmitterData.h"

void ATrailEffectEmitter::StartPlay()
{
	Super::StartPlay();

	ACharacter* Character = Cast<ACharacter>(SecondTarget);
	
	if (Character && !FirstTransform->BindSocket.IsEmpty() && !SecondTransform->BindSocket.IsEmpty())
	{
		PSComponent = NewObject<UParticleSystemComponent>(this);
		PSComponent->RegisterComponent();
		PSComponent->SetTemplate(GetParticleSystemComponent()->Template);
		PSComponent->AttachToComponent(Character->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
		PSComponent->ActivateSystem(true);
		PSComponent->BeginTrails(FName(*FirstTransform->BindSocket), FName(*SecondTransform->BindSocket), WidthScaleMode, 1.0f);

		// 添加透明度模块
		if (EffectEmitterData->ParticleData.bGraduallyHidden || EffectEmitterData->ParticleData.bUseConstAlpha)
		{
			AddAlphaModule(PSComponent);
		}
		//AttachToComponent(Character->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
		//GetParticleSystemComponent()->AttachToComponent(Character->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
		//GetParticleSystemComponent()->ActivateSystem(true);
		//GetParticleSystemComponent()->BeginTrails(FName(*FirstSocket), FName(*SecondSocket), WidthScaleMode, 1.0f);
	}
	else
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Trail effect binding object is not character,please the change binding object"));
	}
	
}

void ATrailEffectEmitter::DelayDestroySetting()
{
	//GetParticleSystemComponent()->EndTrails();
	if (IsValid(PSComponent))
	{
		PSComponent->EndTrails();
	}
}

void ATrailEffectEmitter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (IsValid(PSComponent))
	{
		PSComponent->DestroyComponent();
		PSComponent = nullptr;
	}

	Super::EndPlay(EndPlayReason);
}


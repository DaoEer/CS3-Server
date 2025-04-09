// Copyright 1998-2019 Epic Games, Inc. All Rights Reserved.

#include "CS3ParitcleAnimNotify.h"
#include "Particles/ParticleSystem.h"
#include "Components/SkeletalMeshComponent.h"
#include "ParticleHelper.h"
#include "Kismet/GameplayStatics.h"
#include "Animation/AnimSequenceBase.h"
#include "Particles/ParticleSystemComponent.h"

#if WITH_EDITOR
#include "Logging/MessageLog.h"
#include "Misc/UObjectToken.h"
#endif

#ifdef SEQUENCER_ICESWORD_ON
#include "Particles/ParticleSystemComponent.h"
#include "AnimSequencerInstance.h"
#endif

/////////////////////////////////////////////////////
// UCS3ParitcleAnimNotify

UCS3ParitcleAnimNotify::UCS3ParitcleAnimNotify()
	: Super()
{
	Attached = true;
	Scale = FVector(1.f);
	PSC = nullptr;

#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(192, 255, 99, 255);
#endif // WITH_EDITORONLY_DATA
}

void UCS3ParitcleAnimNotify::SetParNotifyRate(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation, float SeqRate)
{
	Received_SetParNotifySacle(MeshComp,Animation,SeqRate);
}

void UCS3ParitcleAnimNotify::PostLoad()
{
	Super::PostLoad();

	RotationOffsetQuat = FQuat(RotationOffset);
}

#if WITH_EDITOR
void UCS3ParitcleAnimNotify::PostEditChangeProperty(FPropertyChangedEvent& PropertyChangedEvent)
{
	Super::PostEditChangeProperty(PropertyChangedEvent);

	if (PropertyChangedEvent.MemberProperty && PropertyChangedEvent.MemberProperty->GetFName() == GET_MEMBER_NAME_CHECKED(UCS3ParitcleAnimNotify, RotationOffset))
	{
		RotationOffsetQuat = FQuat(RotationOffset);
	}
}

void UCS3ParitcleAnimNotify::ValidateAssociatedAssets()
{
	static const FName NAME_AssetCheck("AssetCheck");

	if ((PSTemplate != nullptr) && (PSTemplate->IsLooping()))
	{
		UObject* ContainingAsset = GetContainingAsset();

		FMessageLog AssetCheckLog(NAME_AssetCheck);

		const FText MessageLooping = FText::Format(
			NSLOCTEXT("AnimNotify", "ParticleSystem_ShouldNotLoop", "Particle system {0} used in anim notify for asset {1} is set to looping, but the slot is a one-shot (it won't be played to avoid leaking a component per notify)."),
			FText::AsCultureInvariant(PSTemplate->GetPathName()),
			FText::AsCultureInvariant(ContainingAsset->GetPathName()));
		AssetCheckLog.Warning()
			->AddToken(FUObjectToken::Create(ContainingAsset))
			->AddToken(FTextToken::Create(MessageLooping));

		if (GIsEditor)
		{
			AssetCheckLog.Notify(MessageLooping, EMessageSeverity::Warning, /*bForce=*/ true);
		}
	}
}
void UCS3ParitcleAnimNotify::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (IsValid(PSC))
	{
		PSC->DestroyComponent();
	}
	Super::StopNotifyEffect(MeshComp, Animation);
}
#endif

void UCS3ParitcleAnimNotify::Notify(class USkeletalMeshComponent* MeshComp, class UAnimSequenceBase* Animation)
{
	// Don't call super to avoid unnecessary call in to blueprints
	UParticleSystemComponent* Component = SpawnParticleSystem(MeshComp, Animation);
#ifdef SEQUENCER_ICESWORD_ON
	if (Component != nullptr)
	{
		UAnimSequencerInstance* SequencerInst = Cast<UAnimSequencerInstance>(MeshComp->GetAnimInstance());
		if (!MeshComp->ISBControler.CopyTo(Component->ISBControler))
			SequencerInst->ICEControler.CopyTo(Component->ISBControler);
	}
#endif
}

FString UCS3ParitcleAnimNotify::GetNotifyName_Implementation() const
{
	if (PSTemplate)
	{
		return PSTemplate->GetName();
	}
	else
	{
		return Super::GetNotifyName_Implementation();
	}
}


UParticleSystemComponent* UCS3ParitcleAnimNotify::SpawnParticleSystem(class USkeletalMeshComponent* MeshComp, class UAnimSequenceBase* Animation)
{
	//PSC = nullptr;
	
	if (PSTemplate)
	{
		if (PSTemplate->IsLooping())
		{
		//	UE_LOG(LogParticles, Warning, TEXT("Particle Notify: Anim '%s' tried to spawn infinitely looping particle system '%s'. Spawning suppressed."), *GetNameSafe(Animation), *GetNameSafe(PSTemplate));
			return PSC;
		}

		if (Attached)
		{
			PSC = UGameplayStatics::SpawnEmitterAttached(PSTemplate, MeshComp, SocketName, LocationOffset, RotationOffset, Scale);
		}
		else
		{
			const FTransform MeshTransform = MeshComp->GetSocketTransform(SocketName);
			FTransform SpawnTransform;
			SpawnTransform.SetLocation(MeshTransform.TransformPosition(LocationOffset));
			SpawnTransform.SetRotation(MeshTransform.GetRotation() * RotationOffsetQuat);
			SpawnTransform.SetScale3D(Scale);
			PSC = UGameplayStatics::SpawnEmitterAtLocation(MeshComp->GetWorld(), PSTemplate, SpawnTransform);
		}
	}
	else
	{
	//	UE_LOG(LogParticles, Warning, TEXT("Particle Notify: Particle system is null for particle notify '%s' in anim: '%s'"), *GetNotifyName(), *GetPathNameSafe(Animation));
	}
	return PSC;
}

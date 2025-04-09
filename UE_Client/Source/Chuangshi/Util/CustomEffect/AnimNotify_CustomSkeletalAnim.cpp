// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_CustomSkeletalAnim.h"
#include "SkeletalAnimParticle.h"
#include "../CS3Debug.h"

#ifdef WITH_EDITOR
#include "ParticleHelper.h"
#endif

#ifdef SEQUENCER_ICESWORD_ON
#include "AnimSequencerInstance.h"
#endif

CONTROL_COMPILE_OPTIMIZE_START

UAnimNotify_CustomSkeletalAnim::UAnimNotify_CustomSkeletalAnim(const FObjectInitializer& ObjectInitializer)
	: Super(),
	MeshScale(1.0f),
	AnimRate(1.0f),
	Attached(true),
	SocketName("rootSocket"),
	BreakWhenAnimStop(false)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(72, 255, 235, 255);
#endif // WITH_EDITORONLY_DATA

	IsWeapon = false;
	UseFadeInAndFadeOut = false;
	UseDissolve = false;
	DissolveTexture = nullptr;
}

/*
const FObjectInitializer& ObjectInitializer

UAnimNotify_CustomSkeletalAnim::UAnimNotify_CustomSkeletalAnim()
	:Super(),
	MeshScale(1.0f),
	AnimRate(1.0f),
	Attached(true),
	SocketName("rootSocket"),
	BreakWhenAnimStop(false)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(72, 255, 235, 255);
#endif // WITH_EDITORONLY_DATA

	IsWeapon = false;
	UseFadeInAndFadeOut = false;
	UseDissolve = false;
	DissolveTexture = nullptr;
}
*/

void UAnimNotify_CustomSkeletalAnim::PostLoad()
{
	Super::PostLoad();
}

#if WITH_EDITOR
void UAnimNotify_CustomSkeletalAnim::PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent)
{
	Super::PostEditChangeProperty(PropertyChangedEvent);
// 	if (PropertyChangedEvent.MemberProperty && PropertyChangedEvent.MemberProperty->GetFName() == GET_MEMBER_NAME_CHECKED(UAnimNotify_PlayParticleEffect, RotationOffset))
// 	{
// 		RotationOffsetQuat = FQuat(RotationOffset);
// 	}
}
#endif

FString UAnimNotify_CustomSkeletalAnim::GetNotifyName_Implementation() const
{
	if (SkeletalMesh)
	{
		return SkeletalMesh->GetName();
	}
	else
	{
		return Super::GetNotifyName_Implementation();
	}
}

void UAnimNotify_CustomSkeletalAnim::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (!SkeletalMesh || !AnimAsset)
	{
		return;
	}
	UWorld* World = MeshComp->GetWorld();
	if (!World)
	{
		return;
	}

	auto Ptr = UStopDelegateStorageComponent::Get(MeshComp);
	if (UStopDelegateStorageComponent::CheckNeedStopNotify(Ptr))
		return;

	SkelParticle = World->SpawnActor<ASkeletalAnimParticle>();
	if (!SkelParticle)
	{
		return;
	}

	if (UseFadeInAndFadeOut)
	{
		SkelParticle->StratFadeInFadeOut(AlphaControl);
	}
		
	if (UseDissolve)
	{
		SkelParticle->StratDissolve(DissolveControl, DissolveTexture);
	}

	if (Attached)
	{
		SkelParticle->GetRootComponent()->AttachToComponent(MeshComp, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
		SkelParticle->GetRootComponent()->SetRelativeLocationAndRotation(LocationOffset, RotationOffset);
	}
	else
	{
		const FTransform MeshTransform = MeshComp->GetSocketTransform(SocketName);
		FTransform SpawnTransform;
		SpawnTransform.SetLocation(MeshTransform.TransformPosition(LocationOffset));
		SpawnTransform.SetRotation(MeshTransform.GetRotation() * FQuat(RotationOffset));

		//SkelParticle->GetRootComponent()->SetRelativeLocationAndRotation(LocationOffset + MeshComp->GetComponentLocation(), RotationOffset);
		SkelParticle->GetRootComponent()->SetRelativeLocationAndRotation(SpawnTransform.GetLocation(), SpawnTransform.GetRotation());
		if (MeshComp->GetOwner())
		{
			//在3D世界中
			SpawnTransform.SetScale3D(MeshComp->GetOwner()->GetActorScale3D() /** Scale*/);
			//光效随模型的状态显示和隐藏
			SkelParticle->SetActorRelativeScale3D(SpawnTransform.GetScale3D());
		}
		else
		{
			//编辑器中
			SpawnTransform.SetScale3D(MeshTransform.GetScale3D() /** Scale*/);
			SkelParticle->SetActorRelativeScale3D(SpawnTransform.GetScale3D());
		}
	}

	if (AnimRateFollowParent)
	{
		AnimRate = Animation->RateScale;
	}

	if (IsWeapon)
	{
		SkelParticle->SetWeapon(IsWeapon);
	}

	bool IsInit = SkelParticle->InitLianRen(MeshComp, SkeletalMesh, AnimAsset, Material, MeshScale,
		AnimStartTime, AnimRate, BindParticle, BindParticleSokect, BreakWhenAnimStop);
	if (!IsInit)
	{
		SkelParticle->Destroy();
	}

	if (IsValid(SkelParticle))
	{
		TWeakObjectPtr<ASkeletalAnimParticle> RefPtr(SkelParticle);
		UStopDelegateStorageComponent::AddStopHandleFunction(Ptr, this, Animation, [RefPtr]() {
			if (RefPtr.IsValid())
				RefPtr.Get()->StopNotifyEffect();
		});
	}


#ifdef SEQUENCER_ICESWORD_ON
	else {
		UAnimSequencerInstance* SequencerInst = Cast<UAnimSequencerInstance>(MeshComp->GetAnimInstance());
		if (!MeshComp->ISBControler.CopyTo(SkelParticle->SkeletalMeshComp->ISBControler) && SequencerInst != nullptr)
			SequencerInst->ICEControler.CopyTo(SkelParticle->SkeletalMeshComp->ISBControler);
		if (!MeshComp->ISBControler.CopyTo(SkelParticle->ISBControler) && SequencerInst != nullptr)
			SequencerInst->ICEControler.CopyTo(SkelParticle->ISBControler); 
	}
#endif
}
void UAnimNotify_CustomSkeletalAnim::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (IsValid(SkelParticle))
	{
		SkelParticle->StopNotifyEffect();
	}
}
CONTROL_COMPILE_OPTIMIZE_END

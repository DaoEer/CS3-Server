// Fill out your copyright notice in the Description page of Project Settings.

#include "AnimNotifyState_AttchSkeletalAnim.h"
#include "../CS3Debug.h"
#include "Components/SkeletalMeshComponent.h"
#include "SkeletalAnimParticle.h"
#include "Animation/AnimSequenceBase.h"

CONTROL_COMPILE_OPTIMIZE_START
UAnimNotifyState_AttchSkeletalAnim::UAnimNotifyState_AttchSkeletalAnim()
{
	SkeletalAnimPle = nullptr;
	SkeletalMesh = nullptr;
	AnimAsset = nullptr;

	#if WITH_EDITORONLY_DATA
		NotifyColor = FColor(255, 236, 0, 255);
	#endif // WITH_EDITORONLY_DATA
}

void UAnimNotifyState_AttchSkeletalAnim::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	Super::NotifyBegin(MeshComp, Animation, TotalDuration);
	
	if (!IsValid(SkeletalMesh) || !IsValid(AnimAsset))
	{
		return;
	}
	UWorld* World = MeshComp->GetWorld();
	if (!IsValid(World))
	{
		return;
	}

	SkeletalAnimPle = World->SpawnActor<ASkeletalAnimParticle>();
	if (!IsValid(SkeletalAnimPle))
	{
		return;
	}

	if (Attached)
	{
		SkeletalAnimPle->GetRootComponent()->AttachToComponent(MeshComp,
			FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
		SkeletalAnimPle->GetRootComponent()->SetRelativeLocationAndRotation(LocationOffset, RotationOffset);
	}
	else
	{
		const FTransform MeshTransform = MeshComp->GetSocketTransform(SocketName);
		FTransform SpawnTransform;
		SpawnTransform.SetLocation(MeshTransform.TransformPosition(LocationOffset));
		SpawnTransform.SetRotation(MeshTransform.GetRotation() * FQuat(RotationOffset));

		SkeletalAnimPle->GetRootComponent()->SetRelativeLocationAndRotation(
			SpawnTransform.GetLocation(), SpawnTransform.GetRotation());
		if (IsValid(MeshComp->GetOwner()))//在游戏中
		{
			SpawnTransform.SetScale3D(MeshComp->GetOwner()->GetActorScale3D() /** Scale*/);
			SkeletalAnimPle->SetActorRelativeScale3D(SpawnTransform.GetScale3D());
		}
		else
		{//在编辑器中预览
			SpawnTransform.SetScale3D(MeshTransform.GetScale3D() /** Scale*/);
			SkeletalAnimPle->SetActorRelativeScale3D(SpawnTransform.GetScale3D());
		}
	}

	float PlayAnimRate = AnimRate;
	if (AnimRateFollowParent)
	{
		PlayAnimRate = Animation->RateScale * AnimRate;
	}

	bool IsInit = SkeletalAnimPle->InitOther(MeshComp, SkeletalMesh, AnimAsset, Scale3DOffset,
		AnimRate, SocketName, true, false);
	if (!IsInit)
	{
		SkeletalAnimPle->Destroy();
	}
}

void UAnimNotifyState_AttchSkeletalAnim::NotifyTick(class USkeletalMeshComponent * MeshComp, 
	class UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	Super::NotifyTick(MeshComp, Animation, FrameDeltaTime);
}

void UAnimNotifyState_AttchSkeletalAnim::NotifyEnd(class USkeletalMeshComponent * MeshComp, 
	class UAnimSequenceBase * Animation)
{
	Super::NotifyEnd(MeshComp, Animation);
	
	if (IsValid(SkeletalAnimPle))
	{
		SkeletalAnimPle->Destroy();
	}
}

void UAnimNotifyState_AttchSkeletalAnim::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (IsValid(SkeletalAnimPle))
	{
		SkeletalAnimPle->StopNotifyEffect();
	}
	Super::StopNotifyEffect(MeshComp,Animation);
}



CONTROL_COMPILE_OPTIMIZE_END

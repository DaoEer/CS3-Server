// Fill out your copyright notice in the Description page of Project Settings.

#include "AnimNotify_AttchSkeletalAnim.h"
#include "UnrealType.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "Actor/GameCharacter.h"
#include "SkeletalAnimParticle.h"
#include "../CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UAnimNotify_AttchSkeletalAnim::UAnimNotify_AttchSkeletalAnim()
{

}

void UAnimNotify_AttchSkeletalAnim::PostLoad()
{
	Super::PostLoad();
}

void UAnimNotify_AttchSkeletalAnim::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
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

	SkeletalAnimPle = World->SpawnActor<ASkeletalAnimParticle>();
	if (!SkeletalAnimPle)
	{
		return;
	}

	if (Attached)
	{
		SkeletalAnimPle->GetRootComponent()->AttachToComponent(MeshComp, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
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
		if (MeshComp->GetOwner())//在游戏中
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
		PlayAnimRate, SocketName, false, true);
	if (!IsInit)
	{
		SkeletalAnimPle->Destroy();
	}
}
void UAnimNotify_AttchSkeletalAnim::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{	
	if (IsValid(SkeletalAnimPle))
	{
		SkeletalAnimPle->StopNotifyEffect();
	}
	Super::StopNotifyEffect(MeshComp, Animation);
}
CONTROL_COMPILE_OPTIMIZE_END
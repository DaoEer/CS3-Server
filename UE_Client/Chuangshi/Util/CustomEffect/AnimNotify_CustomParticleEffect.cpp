// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_CustomParticleEffect.h"
#include "Kismet/GameplayStatics.h"
#include "../../Manager/DecalManager.h"
#include "GameFramework/Actor.h"
#include "Components/SkeletalMeshComponent.h"
#include "Particles/ParticleSystemComponent.h"



//#include "Animation/DebugSkelMeshComponent.h"


UAnimNotify_CustomParticleEffect::UAnimNotify_CustomParticleEffect()
	:Super(),
	Attached(true),
	SocketName("rootSocket"),
	PSC(NULL)
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(0, 145, 255, 255);
#endif // WITH_EDITORONLY_DATA

}

void UAnimNotify_CustomParticleEffect::PostLoad()
{
	Super::PostLoad();

	RotationOffsetQuat = FQuat(RotationOffset);
}

#if WITH_EDITOR
void UAnimNotify_CustomParticleEffect::PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent)
{
	Super::PostEditChangeProperty(PropertyChangedEvent);

	if (PropertyChangedEvent.MemberProperty && PropertyChangedEvent.MemberProperty->GetFName() == GET_MEMBER_NAME_CHECKED(UAnimNotify_PlayParticleEffect, RotationOffset))
	{
		RotationOffsetQuat = FQuat(RotationOffset);
	}
}
#endif

void UAnimNotify_CustomParticleEffect::BeginDestroy()
{
	Super::BeginDestroy();
}

FString UAnimNotify_CustomParticleEffect::GetNotifyName_Implementation() const
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

void UAnimNotify_CustomParticleEffect::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (PSTemplate)
	{
		if (Attached)
		{
			PSC = UGameplayStatics::SpawnEmitterAttached(PSTemplate, MeshComp, SocketName, LocationOffset, RotationOffset);
		}
		else
		{
			const FTransform MeshTransform = MeshComp->GetSocketTransform(SocketName);
			FTransform SpawnTransform;
			SpawnTransform.SetLocation(MeshTransform.TransformPosition(LocationOffset));
			SpawnTransform.SetRotation(MeshTransform.GetRotation() * RotationOffsetQuat);
			PSC = UGameplayStatics::SpawnEmitterAtLocation(MeshComp->GetWorld(), PSTemplate, SpawnTransform);
		}
		_ParticleSysToDecals(MeshComp);
	}
}

void UAnimNotify_CustomParticleEffect::StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (IsValid(PSC))
	{
		PSC->DestroyComponent();
	}
	Super::StopNotifyEffect(MeshComp, Animation);
}

void UAnimNotify_CustomParticleEffect::_ParticleSysToDecals(USkeletalMeshComponent* MeshComp)
{
	// 在切换场景或EndPlay的时候World会删除（并删除world创建的所有Actor）重新创建
	// 所以这里只管创建DecalEffectMgr，不管删除
	UWorld * World = MeshComp->GetWorld();
	if (World)
	{
		TArray<ADecalEffect*> DecalArray = UDecalManager::GetInstance()->CreateDecalEffect(PSTemplate, MeshComp);

		//由于光效通用性的需要，贴花组件全部绑定在本身的粒子上
		for (auto Effect : DecalArray)
		{
			if (Attached)
			{
				Effect->AttachToComponent(MeshComp, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
			}
			else
			{
				Effect->SetActorTransform(MeshComp->GetSocketTransform(SocketName));
			}
			
			Effect->AddActorLocalOffset(LocationOffset);
			Effect->AddActorLocalRotation(RotationOffset);
		}
	}
}

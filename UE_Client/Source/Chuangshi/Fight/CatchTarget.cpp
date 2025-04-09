// Fill out your copyright notice in the Description page of Project Settings.


#include "CatchTarget.h"
#include "Actor/BeCatchedCharacter.h"
#include "Actor/ServerCharacter.h"
#include "Util/CustomEffect/SkeletalAnimParticle.h"
#include "Actor/GameCharacter.h"
#include "Component/AppearanceComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"

void UCatchTarget::CatchTarget(const int32 TargetID, AActor* CurActor,const FName AnimID)
{
	//获取目标
	AServerCharacter* TargetActor = Cast<AServerCharacter>
		(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	//如果目标不存在则不执行
	if (!IsValid(TargetActor) || TargetActor == CurActor)
	{
		return;
	}

	//创建单机目标
	ABeCatchedCharacter* ClientCharacter = UGolbalBPFunctionLibrary::SpawnActor<ABeCatchedCharacter>();

	if (!IsValid(ClientCharacter))
	{
		return;
	}
	//ClientCharacter->InitAppearanceComponent();
	if (!IsValid(ClientCharacter->AppearanceComponent))
	{
		ClientCharacter->Destroy();
		return;
	}

	ClientCharacter->m_AnimId = AnimID;
	ClientCharacter->AppearanceComponent->CopyCharacterFromClientAppearance(TargetActor);
	ClientCharacter->SetActorTransform(TargetActor->GetActorTransform());

	//获取施法者
	AServerCharacter* AtkActor = Cast<AServerCharacter>(CurActor);

	if (!IsValid(AtkActor))
	{
		return;
	}

	//获取链刃铁链
	TArray<AActor*> AttachedActors;
	AtkActor->GetAttachedActors(AttachedActors);

	for (auto AttachedActor : AttachedActors)
	{
		ASkeletalAnimParticle* SkeletalAnimParticle = Cast<ASkeletalAnimParticle>(AttachedActor);

		if (IsValid(SkeletalAnimParticle))
		{
			if (SkeletalAnimParticle->IsWeapon())
			{
				ClientCharacter->AttachToComponent(SkeletalAnimParticle->SkeletalMeshComp,
					FAttachmentTransformRules::KeepWorldTransform, TEXT("Socket_Weapon_L_03"));
				ClientCharacter->SetActorRelativeLocation(FVector::ZeroVector);
				return;
			}
		}
	}
}

void UCatchTarget::ReleaseTarget(AActor* CurActor)
{
	//获取施法者
	AServerCharacter* AtkActor = Cast<AServerCharacter>(CurActor);

	if (!IsValid(AtkActor))
	{
		return;
	}

	//获取链刃铁链
	TArray<AActor*> AttachedActors;
	AtkActor->GetAttachedActors(AttachedActors);

	for (auto AttachedActor : AttachedActors)
	{
		ASkeletalAnimParticle* SkeletalAnimParticle = Cast<ASkeletalAnimParticle>(AttachedActor);

		if (IsValid(SkeletalAnimParticle))
		{
			if (SkeletalAnimParticle->IsWeapon())
			{
				SkeletalAnimParticle->DestroyChilds();
				//SkeletalAnimParticle->Destroy();
				return;
			}

		}
	}
}

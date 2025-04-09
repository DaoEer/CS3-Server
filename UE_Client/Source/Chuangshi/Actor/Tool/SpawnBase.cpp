// Fill out your copyright notice in the Description page of Project Settings.


#include "SpawnBase.h"
#include "Manager/ParticleManager.h"
#include "Particles/ParticleSystemComponent.h"
#include "Util/CS3Debug.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Component/AppearanceComponent.h"

// Sets default values
ASpawnBase::ASpawnBase()
{
	CharacterClassName = TEXT("SpawnBase");
	PrimaryActorTick.bCanEverTick = true;
	IsEffectBind = false;
	CurEffect.Empty();
	IsCanSpawnEffect = true;
	EffectComponent = nullptr;
	InitBaseComponent();
}

void ASpawnBase::SetAnimationOfStand(UDataTable* AnimData)
{
	if (AnimData)
	{
		for (auto object : AnimData->GetRowMap())
		{
			if ("Idle_Free" == object.Key)
			{
				//加载动作
				const FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
				GetMesh()->AnimationData.AnimToPlay = LoadObject<UAnimationAsset>(nullptr, *(ActionData->AnimPath).ToString());
				return;
			}
		}
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Not Find SpawnPoint's Animation!"));

}

void ASpawnBase::PlayEffect(FName EffectID)
{
	//能否看到光效
	if (!IsCanSpawnEffect)
	{
		ClearEffect();
		return;
	}

	UParticleManager* ParticleManager = NewObject<UParticleManager>();
	if (IsValid(ParticleManager))
	{
		//创建光效
		AEffectEmitter* Effect = ParticleManager->PlayParticleOfEdit(EffectID, this);
		if (Effect)
		{
			CurEffect.Add(Effect);
		}
	}

}

void ASpawnBase::EffectStartPlay(FEFFECT_DATA EffectData)
{
	
	if (!EffectData.BaseEffectData.FirstTransform.BindSocket.IsEmpty())
	{
		EffectComponent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, FName(*EffectData.BaseEffectData.FirstTransform.BindSocket));
	}
	else
	{
		EffectComponent->AttachToComponent(GetMesh(), FAttachmentTransformRules::KeepRelativeTransform);
	}

	EffectComponent->SetRelativeTransform(EffectData.BaseEffectData.FirstTransform.Transform);

}

void ASpawnBase::ClearEffect()
{
	for (AEffectEmitter* tempEffect : CurEffect)
	{
		if (tempEffect)
		{
			tempEffect->Destroy();
		}
	}
	CurEffect.Empty();
}

//init component
void ASpawnBase::InitBaseComponent()
{
	GetMesh()->SetAnimationMode(EAnimationMode::AnimationSingleNode);
	AppearanceComponent = CreateDefaultSubobject<UAppearanceComponent>(TEXT("AppearanceComponent"));
	EffectComponent = CreateDefaultSubobject<UParticleSystemComponent>(TEXT("EffectComponent"));
	EffectComponent->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);

}

void ASpawnBase::SetActorPart(MODEL_PART_TYPE PartPos, FMODEL_PART_DATA PartData)
{
	LoadObject<UObject>(nullptr, *PartData.ModelPartPath.ToString()); 
	UObject* PartMesh = PartData.ModelPartPath.Get();
	if (PartMesh)
	{
		AppearanceComponent->AddActorPart(PartPos, PartData);
	}
	else
	{
		AppearanceComponent->CancelActorPart(PartPos);
	}
}

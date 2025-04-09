// Fill out your copyright notice in the Description page of Project Settings.

#include "DecalEffectEmitter.h"
// UE4
#include "Particles/ParticleSystemComponent.h"
// 数据类型
#include "GameData/EffectEmitterData.h"
// CS3类型
#include "Manager/DecalManager.h"
#include "Actor/GameCharacter.h"
#include "Util/CustomEffect/DecalEffect.h"

DECLARE_CYCLE_STAT(TEXT("UpdateTransparency"), STAT_UpdateTransparency, STATGROUP_ADecalEffectEmitter);

TArray<ADecalEffect*> ADecalEffectEmitter::GetDecalArr()
{
	return DecalArr;
}

void ADecalEffectEmitter::StartPlay()
{
	DecalArr = UDecalManager::GetInstance()->CreateDecalEffect(GetParticleSystemComponent()->Template, nullptr);

	//将所有的光效绑定在粒子组件下面
	for (auto Effect : DecalArr)
	{
		Effect->AttachToComponent(GetParticleSystemComponent(), FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
	}

	Super::StartPlay();
}

void ADecalEffectEmitter::DelayDestroySetting()
{
	Super::DelayDestroySetting();

	for (ADecalEffect* Decal : DecalArr)
	{
		Decal->PauseDecal();
	}
}

void ADecalEffectEmitter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	for (ADecalEffect* Decal : DecalArr)
	{
		UDecalManager::GetInstance()->DestroyDecalEffect(Decal);
	}

	Super::EndPlay(EndPlayReason);
}

void ADecalEffectEmitter::UpdateTransparency(float DeltaSeconds)
{
	SCOPE_CYCLE_COUNTER(STAT_UpdateTransparency);

	Super::UpdateTransparency(DeltaSeconds);

	if (EffectEmitterData->ParticleData.bUseConstAlpha)
	{
		for (auto Effect : DecalArr)
		{
			Effect->SetVectorParameter(Alpha * EffectEmitterData->ParticleData.InitAlpha);
		}
	}
	else
	{
		for (auto Effect : DecalArr)
		{
			Effect->SetVectorParameter(Alpha);
		}
	}
}
// Fill out your copyright notice in the Description page of Project Settings.


#include "DecalEffectNewEmitter.h"
#include "ParticleEmitterInstances.h"
#include "Particles/ParticleModule.h"
#include "Particles/ParticleEmitter.h"
#include "Particles/ParticleLODLevel.h"
#include "Particles/ParticleSystemComponent.h"
#include "ParticleModuleEx/ParticleModuleTypeDataDecal.h"
#include "ParticleModuleEx/ParticleDecalEmitterInstances.h"
#include "Components/DecalComponent.h"
#include "Materials/MaterialInstanceDynamic.h"

void ADecalEffectNewEmitter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
}

void ADecalEffectNewEmitter::StartPlay()
{	
	this->GetParticleSystemComponent()->ActivateSystem(true);
	Super::StartPlay();

	UParticleSystemComponent* psComp = this->GetParticleSystemComponent();

	// 获取粒子中贴花组件
	if (psComp->EmitterInstances.Num())
	{
		for (int32 i = 0; i < psComp->EmitterInstances.Num(); i++)
		{
			// 遍历粒子发射器
			FParticleEmitterInstance* Instance = psComp->EmitterInstances[i];
			if (!Instance || !Instance->SpriteTemplate)
				continue;
			
			// 判断这个发射器是否是贴花发射器
			//UParticleLODLevel* LODLevel = Instance->SpriteTemplate->GetLODLevel(0);
			UParticleLODLevel* LODLevel = Instance->SpriteTemplate->GetCurrentLODLevel(Instance);
			if (!LODLevel)
				continue;

			UParticleModuleTypeDataDecal* DecalTypeData = Cast<UParticleModuleTypeDataDecal>(LODLevel->TypeDataModule);
			if (!IsValid(DecalTypeData))
				continue;

			// 把发射器转为贴花类型发射器（贴花组件存储在贴花发射器里）
			FParticleDecalEmitterInstance* Inst = static_cast<FParticleDecalEmitterInstance*>(Instance);
			if (Inst == nullptr)
				continue;

			// 获取贴花材质
			for (int32 j = 0; j < Inst->Decals.Num(); j++)
			{
				UMaterialInterface* Mat = Inst->Decals[j]->GetDecalMaterial();

				UMaterialInstanceDynamic* dyMaterial = Cast<UMaterialInstanceDynamic>(Mat);
				if (!dyMaterial)
					continue;

				//如下设置材质的颜色
				//FLinearColor Color;
				//dyMaterial->SetVectorParameterValue(TEXT("ColorParamEX"), Color);
				//如下设置材质的扭曲——G，溶解——A
				FLinearColor Dynamic;
				dyMaterial->GetVectorParameterValue(TEXT("DynamicParamEX"), Dynamic);

				dyMaterial->SetVectorParameterValue(TEXT("DynamicParamEX"), Dynamic);
			}
		}
	}
}

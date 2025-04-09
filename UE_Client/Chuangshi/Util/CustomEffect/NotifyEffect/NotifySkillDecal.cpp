// Fill out your copyright notice in the Description page of Project Settings.

#include "NotifySkillDecal.h"
#include "Manager/DecalManager.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../DecalEffect.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/ResourceManager.h"
#include "Components/SkeletalMeshComponent.h"
#include "Particles/ParticleSystem.h"


UNotifySkillDecal::UNotifySkillDecal()
{
	///光效资源
	PSTemplate = nullptr;

	///位置
	DecalLocation = FVector::ZeroVector;
	///旋转
	DecalRoater = 0;
	///缩放
	DecalScale = 1.0f;
	///贴花高度
	DecalHight = 100.0f;
	///是否绑定
	bIsBind = true;
	///生命周期
	LifeTime = 1.0f;
	///骨骼点
	SocketName = "Socket_Root";
}



void UNotifySkillDecal::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->ClearObjectHandles(this);
	}
	Super::BeginDestroy();
}

void UNotifySkillDecal::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	Super::Notify(MeshComp, Animation);

	SpawnMat(MeshComp);
}

void UNotifySkillDecal::SpawnMat(USkeletalMeshComponent* MeshComp)
{
	//判断粒子的存在
	if (!IsValid(PSTemplate))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNotifySkillDecal::SpawnMat: PSTemplate!"));
		return;
	}

	TArray<ADecalEffect*> DecalArr = UDecalManager::GetInstance()->CreateDecalEffect(PSTemplate, MeshComp);

	//由于光效通用性的需要，贴花组件全部绑定在本身的粒子上
	for (auto Effect : DecalArr)
	{
		if (bIsBind)
		{
			Effect->AttachToComponent(MeshComp, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false), SocketName);
		}
		else
		{
			Effect->SetActorTransform(MeshComp->GetSocketTransform(SocketName));
		}
		Effect->AddActorLocalOffset(DecalLocation);
		Effect->AddActorLocalRotation(FRotator(0, DecalRoater, 0));
		Effect->SetActorRelativeScale3D(FVector(DecalHight / 100.f, DecalScale, DecalScale));
	}

	//处理延时
	FTimerHandle DelayHandle;

	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle,
			FTimerDelegate::CreateLambda([DecalArr]() {
			for (ADecalEffect* Decal : DecalArr)
			{
				UDecalManager::GetInstance()->DestroyDecalEffect(Decal);
			}

		}), LifeTime, false);
	}
	else
	{
		MeshComp->GetWorld()->GetTimerManager().SetTimer(DelayHandle,
			FTimerDelegate::CreateLambda([DecalArr]() {
			for (ADecalEffect* Decal : DecalArr)
			{
				UDecalManager::GetInstance()->DestroyDecalEffect(Decal);
			}

		}), LifeTime, false);
	}
}


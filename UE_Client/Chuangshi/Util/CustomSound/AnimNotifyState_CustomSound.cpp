// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotifyState_CustomSound.h"
#include "CustomSound.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/AudioManager.h"
#include "../CS3Debug.h"
#include "../GolbalBPFunctionLibrary.h"

UAnimNotifyState_CustomSound::UAnimNotifyState_CustomSound()
{
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(196, 142, 255, 255);
#endif // WITH_EDITORONLY_DATA
	VolumeMultiplier = 1.0f;
	PitchMultiplier = 1.0f;
	bIsBind = false;
	BindName = FName();
}

void UAnimNotifyState_CustomSound::NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	if (CurSoundMap.Contains(MeshComp) && IsValid(*CurSoundMap.Find(MeshComp)))
	{
		(*CurSoundMap.Find(MeshComp))->Stop();
		CurSoundMap.Remove(MeshComp);
	}

	if (!IsValid(MeshComp) || !IsValid(Animation))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAnimNotifyState_CustomSound::NotifyBegin: MeshComp ||Animation!"));
		return;
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		if (!UUECS3GameInstance::Instance->AudioManager->CheckPlayVoice(CSTORY_VOICE_TYPE::SOUND3D))
		{
			return;
		}
	}

	//CST-9132删除括号的内容解决9132问题(&& Sound->IsLooping()不是循环音效则无法播放)
	if (IsValid(Sound))
	{
		UWorld* ComponentWorld = MeshComp->GetWorld();

		if (!IsValid(ComponentWorld))
		{
			return;
		}

		ACustomSound* CurSound = nullptr;
		
#if WITH_EDITOR
		//创建音效
		FActorSpawnParameters SpawnParameters;
		SpawnParameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		CurSound = ComponentWorld->SpawnActor<ACustomSound>(ACustomSound::StaticClass(),
			MeshComp->GetComponentLocation(), FRotator(0, 0, 0), SpawnParameters);
#else
		CurSound = UGolbalBPFunctionLibrary::SpawnActor<ACustomSound>(ACustomSound::StaticClass(),
			MeshComp->GetComponentLocation(), FRotator(0, 0, 0));
#endif
			if (IsValid(CurSound))
			{
				//初始化数据
				CurSound->InitCustomSound(Sound, VolumeMultiplier, PitchMultiplier, 0.0f);

				if (bIsBind)
				{
					//绑定到身上
					CurSound->AttachToComponent(MeshComp, FAttachmentTransformRules::KeepRelativeTransform, BindName);
				}

				CurSoundMap.Add(MeshComp, CurSound);
			}
	}
}

void UAnimNotifyState_CustomSound::NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime)
{

}

void UAnimNotifyState_CustomSound::NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation)
{
	if (CurSoundMap.Contains(MeshComp) && IsValid(*CurSoundMap.Find(MeshComp)))
	{
		(*CurSoundMap.Find(MeshComp))->Stop();
		CurSoundMap.Remove(MeshComp);
	}
}

FString UAnimNotifyState_CustomSound::GetNotifyName_Implementation() const
{
	if (Sound)
	{
		return Sound->GetName();
	}
	else
	{
		return Super::GetNotifyName_Implementation();
	}
}

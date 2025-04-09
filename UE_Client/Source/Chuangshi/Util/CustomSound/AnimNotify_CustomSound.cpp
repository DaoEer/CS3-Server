// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_CustomSound.h"
#include "CustomSound.h"
#include "Sound/SoundBase.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/AudioManager.h"
#include "../CS3Debug.h"
#include "../GolbalBPFunctionLibrary.h"


CONTROL_COMPILE_OPTIMIZE_START
UAnimNotify_CustomSound::UAnimNotify_CustomSound()
{
	Sound = nullptr;
	StartTime = 0.0f;
	VolumeMultiplier = 1.0f;
	PitchMultiplier = 1.0f;
	bIsBind = false;
	BindName = FName();
#if WITH_EDITORONLY_DATA
	NotifyColor = FColor(196, 142, 255, 255);
#endif // WITH_EDITORONLY_DATA
}

FString UAnimNotify_CustomSound::GetNotifyName_Implementation() const
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

void UAnimNotify_CustomSound::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (!IsValid(MeshComp) || !IsValid(Animation))
	{
		CS3_Warning(TEXT("-->Null Pointer error:ASkeletalAnimParticle::OnCheckWeaponBindObj: MeshComp ||Animation!"));
		return;
	}

	if (CurSoundMap.Contains(MeshComp) && IsValid(*CurSoundMap.Find(MeshComp)))
	{
		(*CurSoundMap.Find(MeshComp))->Stop();
		CurSoundMap.Remove(MeshComp);
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		if (!UUECS3GameInstance::Instance->AudioManager->CheckPlayVoice(CSTORY_VOICE_TYPE::SOUND3D))
		{
			return;
		}
	}

	if (IsValid(Sound))
	{
		if (Sound->IsLooping())
		{
			return;
		}

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
			FCustomSoundFinished SoundFinishedDele;
			SoundFinishedDele.AddUObject(this, &UAnimNotify_CustomSound::OnCurSoundFinish);

			//初始化数据
			CurSound->InitCustomSound(Sound, VolumeMultiplier, PitchMultiplier, StartTime, SoundFinishedDele);

			if (bIsBind)
			{
				//绑定到身上
				CurSound->AttachToComponent(MeshComp, FAttachmentTransformRules::KeepRelativeTransform, BindName);
			}

			CurSoundMap.Add(MeshComp, CurSound);
		}
	}
}

void UAnimNotify_CustomSound::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (!IsValid(MeshComp) || !IsValid(Animation))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UAnimNotify_CustomSound::StopNotifyEffect: MeshComp ||Animation!"));
		return;
	}

	if (CurSoundMap.Contains(MeshComp) && IsValid(*CurSoundMap.Find(MeshComp)))
	{
		(*CurSoundMap.Find(MeshComp))->Stop();
		CurSoundMap.Remove(MeshComp);
	}
}

void UAnimNotify_CustomSound::OnCurSoundFinish(ACustomSound* FinishSound)
{
	USkeletalMeshComponent* TemMesh = *CurSoundMap.FindKey(FinishSound);

	if (IsValid(TemMesh))
	{
		CurSoundMap.Remove(TemMesh);
	}
}
CONTROL_COMPILE_OPTIMIZE_END

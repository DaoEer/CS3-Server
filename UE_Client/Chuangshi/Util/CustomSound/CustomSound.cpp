// Fill out your copyright notice in the Description page of Project Settings.


#include "CustomSound.h"
#include "Components/AudioComponent.h"
#include "Util/CS3Debug.h"
#include "Sound/SoundBase.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/AudioManager.h"
#include "Util/GolbalBPFunctionLibrary.h"


// Sets default values
ACustomSound::ACustomSound()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	//添加声音组件
	m_AudioComponent = CreateDefaultSubobject<UCS3AudioComponent>(TEXT("AudioComponent"));
	SetRootComponent(m_AudioComponent);
	m_AudioComponent->OnVirtualAudioFinishedNative.AddUObject(this, &ACustomSound::OnAudioFinished);
}

void ACustomSound::InitCustomSound(class USoundBase* Sound,float VolumeMultiplier, float PitchMultiplier, float StartTime,FCustomSoundFinished Finished)
{
	if (IsValid(m_AudioComponent) && IsValid(Sound))
	{
		UWorld* ComponentWorld = m_AudioComponent->GetWorld();

		if (IsValid(ComponentWorld))
		{
			const bool bIsInGameWorld = ComponentWorld->IsGameWorld();

			m_AudioComponent->SetSound(Sound);//资源加入			
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
			{
				VolumeMultiplier = UGolbalBPFunctionLibrary::AudioManager()->GetEffVol();					
			}			
			m_AudioComponent->SetVolumeMultiplier(VolumeMultiplier);//设置音量因子
			m_AudioComponent->SetPitchMultiplier(PitchMultiplier);//设置音高因子
			m_AudioComponent->bAllowSpatialization = bIsInGameWorld;
			m_AudioComponent->bIsUISound = !bIsInGameWorld;//是否为UI音效
			m_AudioComponent->bAutoDestroy = false;//不会自动销毁
			m_AudioComponent->SubtitlePriority = Sound->GetSubtitlePriority();
			m_AudioComponent->Play(StartTime);//开始
		}

		OnSoundFinished = Finished;
	}
	else
	{
		CS3_Warning(TEXT("ACustomSound::InitCustomSound--- Sound Is Null!"))
	}
}

void ACustomSound::Stop()
{
	if (IsValid(m_AudioComponent))
	{
		m_AudioComponent->Stop();
	}

	if (OnSoundFinished.IsBound())
	{
		OnSoundFinished.Broadcast(this);
		OnSoundFinished.Clear();
	}

	this->Destroy();
}

void ACustomSound::OnAudioFinished(UAudioComponent* curAudio)
{
	Stop();
}


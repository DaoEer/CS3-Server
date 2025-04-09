#include "CS3AudioComponent.h"
#include "Engine/World.h"
#include "TimerManager.h"

UCS3AudioComponent::UCS3AudioComponent(const FObjectInitializer& ObjectInitializer)
{
	// 将虚拟音频完成事件与音频完成事件关联
	OnAudioFinishedNative.AddWeakLambda(this, [this](UAudioComponent* _This) {OnVirtualAudioFinished_Internal(); });
}

void UCS3AudioComponent::OnVirtualAudioFinished_Internal()
{
	bIsVirtualActive = false;
	OnVirtualAudioFinished.Broadcast();
	OnVirtualAudioFinishedNative.Broadcast(this);
}

void UCS3AudioComponent::FadeOut(float FadeOutDuration, float FadeVolumeLevel)
{
	if (bIsVirtualActive && !bIsActive)
	{
		OnVirtualAudioFinished_Internal();
	}

	UAudioComponent::FadeOut(FadeOutDuration, FadeVolumeLevel);
}

void UCS3AudioComponent::Play(float StartTime)
{
	UAudioComponent::Play(StartTime);

	if (bIsVirtualActive)	// 如果已经有在虚拟音频播放的话立即完成播放
	{
		OnVirtualAudioFinished_Internal();
	}

	if (!bIsActive && Sound)	// 在播放失败时才使用计时模拟音频播放
	{
		bIsVirtualActive = true;
		GetWorld()->GetTimerManager().SetTimer(VirtualAudioTimerHandle, this, &UCS3AudioComponent::OnVirtualAudioFinished_Internal, Sound->GetDuration() - StartTime);
	}
	else
	{
		GetWorld()->GetTimerManager().ClearTimer(VirtualAudioTimerHandle);
	}
}

void UCS3AudioComponent::Stop()
{
	if (bIsVirtualActive && !bIsActive)
	{
		OnVirtualAudioFinished_Internal();
	}

	UAudioComponent::Stop();
}

void UCS3AudioComponent::SetPaused(bool bPause)
{
	UAudioComponent::SetPaused(bPause);
	if (bPause)
	{
		GetWorld()->GetTimerManager().PauseTimer(VirtualAudioTimerHandle);
	}
	else
	{
		GetWorld()->GetTimerManager().UnPauseTimer(VirtualAudioTimerHandle);
	}
}

bool UCS3AudioComponent::IsPlaying() const
{
	return bIsVirtualActive || bIsActive;
}
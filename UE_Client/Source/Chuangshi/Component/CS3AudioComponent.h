#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "Engine/EngineTypes.h"
#include "Components/SceneComponent.h"
#include "Components/AudioComponent.h"

#include "CS3AudioComponent.generated.h"

UENUM()
enum class Load_Assert_State : uint8
{
	Assert_None = 0,			///无音效资源
	Assert_Loading = 1,			///正在加载资源（异步）
	Assert_Ready = 2,			///资源加载完毕

};


UCLASS(ClassGroup = (Audio, Common), hidecategories = (Object, ActorComponent, Physics, Rendering, Mobility, LOD), ShowCategories = Trigger, meta = (BlueprintSpawnableComponent))
class UCS3AudioComponent : public UAudioComponent
{
	GENERATED_BODY()
public:
	UCS3AudioComponent(const FObjectInitializer& ObjectInitializer);
public:
	/* 
		不管是否是虚拟音频模拟,这个事件都会触发
		UCS3AudioComponent::OnAudioFinished事件触发也会触发该事件 
	*/
	UPROPERTY(BlueprintAssignable)
	FOnAudioFinished OnVirtualAudioFinished;
	//	行为与OnVirtualAudioFinished一致
	FOnAudioFinishedNative OnVirtualAudioFinishedNative;

public:	/* UCS3AudioComponent接口 */
	virtual	void FadeOut(float FadeOutDuration, float FadeVolumeLevel) override;
	virtual void Play(float StartTime = 0.f) override;
	virtual void Stop() override;
	void SetPaused(bool bPause);
	virtual bool IsPlaying() const override;

	FORCEINLINE void SetAssertLoadState(Load_Assert_State NewState) { LAssertState = NewState; }
	FORCEINLINE bool IsAssertLoadState(Load_Assert_State State) { return LAssertState == State; }

private:
	//	声音播放计时器句柄(用于在音频无法播放时虚拟播放, http://172.16.2.227/browse/CST-8873)
	FTimerHandle VirtualAudioTimerHandle;

	//	只有在模拟虚拟音频的时候才会是true
	bool bIsVirtualActive = false;

	UPROPERTY()
	Load_Assert_State LAssertState;
private:
	void OnVirtualAudioFinished_Internal();
};
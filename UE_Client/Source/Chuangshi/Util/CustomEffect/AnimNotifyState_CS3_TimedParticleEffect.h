#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "CS3AnimNotifyState.h"
#include "AnimNotifyState_CS3_TimedParticleEffect.generated.h"
class UParticleSystem;
class USkeletalMeshComponent;
class UProperty;
class UAnimSequenceBase;
class UParticleSystemComponent;

UCLASS(const, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3 Timed Particle Effect"))
class CHUANGSHI_API UAnimNotifyState_CS3_TimedParticleEffect : public UCS3AnimNotifyState
{
	GENERATED_UCLASS_BODY()

	// The particle system template to use when spawning the particle component
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (ToolTip = "The particle system to spawn for the notify state"))
		UParticleSystem* PSTemplate;

	// The socket within our mesh component to attach to when we spawn the particle component
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (ToolTip = "The socket or bone to attach the system to"))
		FName SocketName;

	// Offset from the socket / bone location
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (ToolTip = "Offset from the socket or bone to place the particle system"))
		FVector LocationOffset;

	// Offset from the socket / bone rotation
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (ToolTip = "Rotation offset from the socket or bone for the particle system"))
		FRotator RotationOffset;

	// Offset from the socket / bone rotation
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (ToolTip = "特效播放速率 （光效播放速度与来源动画的播放速度无关）"))
		float EffectRate = 1.0f;

	// Whether or not we destroy the component at the end of the notify or instead just stop
	// the emitters.
	UPROPERTY(EditAnywhere, Category = ParticleSystem, meta = (DisplayName = "Destroy Immediately", ToolTip = "Whether the particle system should be immediately destroyed at the end of the notify state or be allowed to finish"))
		bool bDestroyAtEnd;

#if WITH_EDITORONLY_DATA
	// The following arrays are used to handle property changes during a state. Because we can't
	// store any stateful data here we can't know which emitter is ours. The best metric we have
	// is an emitter on our Mesh Component with the same template and socket name we have defined.
	// Because these can change at any time we need to track previous versions when we are in an
	// editor build. Refactor when stateful data is possible, tracking our component instead.
	UPROPERTY(transient)
		TArray<UParticleSystem*> PreviousPSTemplates;

	UPROPERTY(transient)
		TArray<FName> PreviousSocketNames;

#endif

#if WITH_EDITOR
	virtual void PreEditChange(UProperty* PropertyAboutToChange) override;
#endif

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;

	// Overridden from UAnimNotifyState to provide custom notify name.
	FString GetNotifyName_Implementation() const override;

private:
	bool ValidateParameters(USkeletalMeshComponent* MeshComp);
	void PreNotifyBegin(class USkeletalMeshComponent * MeshComp);
	void SpawnEmitterByOwnerVisiblity(class USkeletalMeshComponent * MeshComp);	
private:
	bool bHiddenInGameOfOwner = false;
	bool bIsSpawnParticleSystemComp = false;

public:
	//UPROPERTY()
	UParticleSystemComponent* PSC;
};
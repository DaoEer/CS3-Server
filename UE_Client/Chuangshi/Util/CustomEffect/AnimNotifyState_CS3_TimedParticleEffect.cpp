#include "AnimNotifyState_CS3_TimedParticleEffect.h"
#include "UnrealType.h"
#include "UObjectGlobals.h"
#include "Engine/World.h"
#include "Engine/Public/TimerManager.h"
#include "Engine/Classes/GameFramework/Actor.h"
#include "Engine/Classes/Components/SceneComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "Components/SkeletalMeshComponent.h"
#include "Particles/ParticleSystemComponent.h"
#include "Kismet/GameplayStatics.h"
#include "SequencerAssistant.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UAnimNotifyState_CS3_TimedParticleEffect::UAnimNotifyState_CS3_TimedParticleEffect(const FObjectInitializer& ObjectInitializer) 
: Super(ObjectInitializer)
{
	PSTemplate = nullptr;
	LocationOffset.Set(0.0f, 0.0f, 0.0f);
	RotationOffset = FRotator(0.0f, 0.0f, 0.0f);
	PSC = nullptr;
}

void UAnimNotifyState_CS3_TimedParticleEffect::NotifyBegin(USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration)
{
	bStopNotifyEffect = false;
	PreNotifyBegin(MeshComp);
	Received_NotifyBegin(MeshComp, Animation, TotalDuration);
}

void UAnimNotifyState_CS3_TimedParticleEffect::NotifyTick(USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime)
{
	if (bStopNotifyEffect)
	{
		return;
	}
	SpawnEmitterByOwnerVisiblity(MeshComp);
	Received_NotifyTick(MeshComp, Animation, FrameDeltaTime);
}

void UAnimNotifyState_CS3_TimedParticleEffect::NotifyEnd(USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation)
{
	TArray<USceneComponent*> Children;
	MeshComp->GetChildrenComponents(false, Children);

	for (USceneComponent* Component : Children)
	{
		if (UParticleSystemComponent* ParticleComponent = Cast<UParticleSystemComponent>(Component))
		{
			bool bSocketMatch, bTemplateMatch;
			bSocketMatch = ParticleComponent->GetAttachSocketName() == SocketName;
			bTemplateMatch = ParticleComponent->Template == PSTemplate;

#if WITH_EDITORONLY_DATA
			// In editor someone might have changed our parameters while we're ticking; so check 
			// previous known parameters too.
			bSocketMatch |= PreviousSocketNames.Contains(ParticleComponent->GetAttachSocketName());
			bTemplateMatch |= PreviousPSTemplates.Contains(ParticleComponent->Template);
#endif

			if (bSocketMatch && bTemplateMatch && !ParticleComponent->bWasDeactivated)
			{
				// Either destroy the component or deactivate it to have it's active particles finish.
				// The component will auto destroy once all particle are gone.
				if (bDestroyAtEnd)
				{
					ParticleComponent->DestroyComponent();
				}
				else
				{
					ParticleComponent->DeactivateSystem();
				}

#if WITH_EDITORONLY_DATA
				// No longer need to track previous values as we've found our component
				// and removed it.
				PreviousPSTemplates.Empty();
				PreviousSocketNames.Empty();
#endif
				// Removed a component, no need to continue
				break;
			}
		}
	}

	Received_NotifyEnd(MeshComp, Animation);
}

bool UAnimNotifyState_CS3_TimedParticleEffect::ValidateParameters(USkeletalMeshComponent* MeshComp)
{
	bool bValid = true;

	if (!PSTemplate)
	{
		bValid = false;
	}
// 	else if (!MeshComp->DoesSocketExist(SocketName) && MeshComp->GetBoneIndex(SocketName) == INDEX_NONE)
// 	{
// 		bValid = false;
// 	}

	return bValid;
}

void UAnimNotifyState_CS3_TimedParticleEffect::PreNotifyBegin(USkeletalMeshComponent * MeshComp)
{	// Only spawn if we've got valid params
	bIsSpawnParticleSystemComp = false;
	if (ValidateParameters(MeshComp))
	{
		auto Ptr = UStopDelegateStorageComponent::Get(MeshComp);
		if (UStopDelegateStorageComponent::CheckNeedStopNotify(Ptr))
			return;
		if (IsValid(MeshComp->GetOwner()))
		{
			bHiddenInGameOfOwner = MeshComp->GetOwner()->bHidden;
		}
		if (!bHiddenInGameOfOwner)
		{
			PSC = UGameplayStatics::SpawnEmitterAttached(PSTemplate, MeshComp, SocketName, LocationOffset, RotationOffset, EAttachLocation::KeepRelativeOffset, !bDestroyAtEnd);
			PSC->CustomTimeDilation = EffectRate;
			bIsSpawnParticleSystemComp = true;
			TWeakObjectPtr<UParticleSystemComponent> RefPtr(PSC);
			UStopDelegateStorageComponent::AddStopHandleFunction(Ptr, this, MeshComp, [=]() {
				if (RefPtr.IsValid())
				{
					if (bDestroyAtEnd)
						RefPtr.Get()->DestroyComponent();
					else
						RefPtr.Get()->DeactivateSystem();
				}
			});

		}
	}
}

void UAnimNotifyState_CS3_TimedParticleEffect::SpawnEmitterByOwnerVisiblity(class USkeletalMeshComponent * MeshComp)
{
	if (IsValid(MeshComp) && IsValid(MeshComp->GetOwner()))
	{
		bool ChangeHideInGame = (MeshComp->GetOwner()->bHidden == bHiddenInGameOfOwner) ? false : true;
		bHiddenInGameOfOwner = MeshComp->GetOwner()->bHidden;
		if (!bIsSpawnParticleSystemComp && !bHiddenInGameOfOwner)
		{
			UWorld* World = MeshComp->GetWorld();
			if (World)
			{
				TWeakObjectPtr<UAnimNotifyState_CS3_TimedParticleEffect> DelayThisPtr(this);
				World->GetTimerManager().SetTimerForNextTick(FTimerDelegate::CreateLambda([DelayThisPtr, MeshComp, this]()
				{
					if (DelayThisPtr.IsValid())
					{
						UAnimNotifyState_CS3_TimedParticleEffect* ParticleEffect = DelayThisPtr.Get();
						if (IsValid(MeshComp) && !ParticleEffect->bIsSpawnParticleSystemComp)
						{
							PSC = UGameplayStatics::SpawnEmitterAttached(ParticleEffect->PSTemplate, MeshComp, ParticleEffect->SocketName, ParticleEffect->LocationOffset, ParticleEffect->RotationOffset, EAttachLocation::KeepRelativeOffset, !(ParticleEffect->bDestroyAtEnd));
							ParticleEffect->bIsSpawnParticleSystemComp = true;
						}
					}
				}));
			}
		}
	}
}

FString UAnimNotifyState_CS3_TimedParticleEffect::GetNotifyName_Implementation() const
{
	if (PSTemplate)
	{
		return PSTemplate->GetName();
	}

	return UAnimNotifyState::GetNotifyName_Implementation();
}

#if WITH_EDITOR
void UAnimNotifyState_CS3_TimedParticleEffect::PreEditChange(UProperty* PropertyAboutToChange)
{
	if (PropertyAboutToChange)
	{
		if (PropertyAboutToChange->GetName() == GET_MEMBER_NAME_STRING_CHECKED(UAnimNotifyState_CS3_TimedParticleEffect, PSTemplate) && PSTemplate != NULL)
		{
			PreviousPSTemplates.Add(PSTemplate);
		}

		if (PropertyAboutToChange->GetName() == GET_MEMBER_NAME_STRING_CHECKED(UAnimNotifyState_CS3_TimedParticleEffect, SocketName) && SocketName != FName(TEXT("None")))
		{
			PreviousSocketNames.Add(SocketName);
		}
	}
}
#endif
CONTROL_COMPILE_OPTIMIZE_END
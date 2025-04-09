// Fill out your copyright notice in the Description page of Project Settings.


#include "AnimNotify_PlayRandonFaceAnim.h"
#include "Engine/World.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "Actor/Action/BaseAnimInstance.h"
#include "Actor/GameCharacter.h"
#include "Actor/Action/HeadBaseAnimInstance.h"
#include "../CS3Debug.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "TimerManager.h"
#include "Actor/Player/StoryCharacter.h"
#include "Manager/ActionManager.h"
#include "Animation/AnimComposite.h"
#include "Animation/BlendSpaceBase.h"

CONTROL_COMPILE_OPTIMIZE_START

UAnimNotify_PlayRandonFaceAnim::UAnimNotify_PlayRandonFaceAnim()
{
	AnimSequence = nullptr;
	CurMeshComp = nullptr;
	CurAnimation = nullptr;
}

void UAnimNotify_PlayRandonFaceAnim::PostLoad()
{
	Super::PostLoad();
}

void UAnimNotify_PlayRandonFaceAnim::Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)
{
	if (!IsValid(AnimSequence))
	{
		return;
	}
	CurMeshComp = MeshComp;
	CurAnimation = Animation;
	UWorld* World = CurMeshComp->GetWorld();
	if (!IsValid(World))
	{
		return;
	}
	AGameCharacter *GameCharacter = Cast<AGameCharacter>(CurMeshComp->GetOwner());
	if (!IsValid(GameCharacter))
	{
		return;
	}

	USkeletalMeshComponent* HeadMeshCpt = Cast<USkeletalMeshComponent>(GameCharacter->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HEADS));
	if (IsValid(HeadMeshCpt))
	{
		HeadBaseAnim = Cast<UHeadBaseAnimInstance>(HeadMeshCpt->GetAnimInstance());
		if (HeadBaseAnim.Get())
		{
			UBaseAnimInstance* BaseAnimInstance = Cast<UBaseAnimInstance>(CurMeshComp->GetAnimInstance());
			AStoryCharacter* StoryCharacter = Cast<AStoryCharacter>(GameCharacter);
			if (IsValid(StoryCharacter))//表示是剧情里面的角色（剧情里面角色没有动画蓝图的）
			{
				CurAnimMontage = HeadBaseAnim.Get()->PlaySlotAnimationAsDynamicMontage(AnimSequence, "DefaultSlot", 0.0f, 0.0f);
			}
			else
			{
				if (IsValid(BaseAnimInstance))
				{
					bool IsPass = false;
					FACTION_DATA CurActionData = BaseAnimInstance->GetCurPlayActionData();
					if (CurActionData.Id.IsNone())
					{
						return;
					}

					if (CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_QEQUENCE)
					{
						IsPass = CurAnimation == CurActionData.CurAnimSquenceBase;
					}
					else if (CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_COMPOSITE)
					{
						UAnimComposite* AnimComposite = Cast<UAnimComposite>(CurActionData.CurAnimSquenceBase);
						if (IsValid(AnimComposite))
						{
							int32 length = AnimComposite->AnimationTrack.AnimSegments.Num();
							for (int32 i = 0; i < length; i++)
							{
								FAnimSegment AnimSegment = AnimComposite->AnimationTrack.AnimSegments[i];
								if (CurAnimation == AnimSegment.AnimReference)
								{
									IsPass = true;
									break;
								}
							}
						}
					}
					else if (CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE ||
						CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_BLEND_SPACE_1D || 
						CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE ||
						CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_OFFSET_BLEND_SAPCE_1D)
					{
						if (IsValid(CurActionData.CurBlendSpaceBase))
						{
							int32 length = CurActionData.CurBlendSpaceBase->GetBlendSamples().Num();
							for (int32 i = 0; i < length; i++)
							{
								FBlendSample BlendSample = CurActionData.CurBlendSpaceBase->GetBlendSamples()[i];
								UAnimSequenceBase* AnimationBase = Cast<UAnimSequenceBase>(BlendSample.Animation);
								if (CurAnimation == AnimationBase)
								{
									IsPass = true;
									break;
								}
							}

						}
					}
					else if (CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_MONTAGE ||
						CurActionData.AnimType == ANIM_TYPE_ENUM::ANIM_TYPE_DYNAMIC_MONTAGE)
					{
						UAnimMontage* AnimMontate = Cast<UAnimMontage>(CurActionData.CurAnimSquenceBase);
						if (IsValid(AnimMontate))
						{
							TArray<UAnimSequenceBase*> AllAnimationAssets;
							for (auto Iter = AnimMontate->SlotAnimTracks.CreateConstIterator(); Iter; ++Iter)
							{
								const FSlotAnimationTrack& Track = (*Iter);
								for (int32 I = 0; I < Track.AnimTrack.AnimSegments.Num(); ++I)
								{
									const struct FAnimSegment& Segment = Track.AnimTrack.AnimSegments[I];
									if (IsValid(Segment.AnimReference))
									{
										AllAnimationAssets.AddUnique(Segment.AnimReference);
									}
								}
							}
							int32 length = AllAnimationAssets.Num();
							for (int32 i = 0; i < length; i++)
							{
								UAnimSequenceBase* SequenceBase = AllAnimationAssets[i];
								if (CurAnimation == SequenceBase)
								{
									IsPass = true;
									break;
								}
							}
						}
					}

					if (IsPass)
					{
						CurAnimMontage = HeadBaseAnim.Get()->PlaySlotAnimationAsDynamicMontage(AnimSequence, "DefaultSlot", 0.0f, 0.0f);
					}
				}
			}
		}
	}
}
void UAnimNotify_PlayRandonFaceAnim::StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation)
{
	if (IsValid(CurAnimMontage) && IsValid(HeadBaseAnim.Get()) && IsValid(AnimSequence) &&
		HeadBaseAnim.Get()->IsPlayingSlotAnimation(AnimSequence, "DefaultSlot", CurAnimMontage))
	{
		HeadBaseAnim.Get()->StopSlotAnimation(0.0f, "DefaultSlot");
	}
}
CONTROL_COMPILE_OPTIMIZE_END


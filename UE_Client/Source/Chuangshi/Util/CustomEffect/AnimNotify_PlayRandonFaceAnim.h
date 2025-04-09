// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotify.h"
#include "Animation/AnimSequenceBase.h"
#include "GameData/CharacterData.h"
#include "AnimNotify_PlayRandonFaceAnim.generated.h"

/**
 *
 */
class UHeadBaseAnimInstance;

UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotify_PlayRandonFaceAnim"))
class CHUANGSHI_API UAnimNotify_PlayRandonFaceAnim : public UCS3AnimNotify
{
	GENERATED_BODY()
public:
	UAnimNotify_PlayRandonFaceAnim();
	virtual void PostLoad() override;
	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
private:
public:
	///¶¯»­×ÊÔ´
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		UAnimSequenceBase* AnimSequence;

private:
	UPROPERTY()
		USkeletalMeshComponent* CurMeshComp;

	UPROPERTY()
		UAnimSequenceBase* CurAnimation;
	UPROPERTY()
		UAnimMontage* CurAnimMontage;
	UPROPERTY()
		TWeakObjectPtr<class UHeadBaseAnimInstance> HeadBaseAnim;
};

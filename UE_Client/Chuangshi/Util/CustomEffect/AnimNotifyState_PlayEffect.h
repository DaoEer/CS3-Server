// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "AnimNotifyState_PlayEffect.generated.h"

/*
* 文件名称：AnimNotifyState_PlayEffect.h
* 功能说明：[通知状态]插槽光效表里面的ID(配置表：DT_EffectCfg)
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-06-19
*/

UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotifyState_PlayEffect"))
class CHUANGSHI_API UAnimNotifyState_PlayEffect : public UCS3AnimNotifyState
{
	GENERATED_UCLASS_BODY()

public:
	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)override;
private:

public:

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "UAnimNotifyState_PlayEffect")
		FString NotifyType = "UAnimNotifyState_PlayEffect";

	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_PlayEffect", DisplayName = "备注")
		FString HelpDesc;

	///绑定光效ID【配置表：DT_EffectCfg】
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "UAnimNotifyState_PlayEffect", DisplayName = "EffectID")
		FString EffectID = "";

private:
	int32 EffectUID = 0;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Util/CustomEffect/CS3AnimNotify.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimSequenceBase.h"
#include "AnimNotify_PlayEffect.generated.h"

/*
* 文件名称：AnimNotify_PlayEffect.h
* 功能说明：[通知]插槽光效表里面的ID(配置表：DT_EffectCfg)
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-06-19
*/

UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotify_PlayEffect"))
class CHUANGSHI_API UAnimNotify_PlayEffect : public UCS3AnimNotify
{
	GENERATED_BODY()

public:
	UAnimNotify_PlayEffect();
	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)override;

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "UAnimNotify_PlayEffect")
		FString NotifyType = "UAnimNotify_PlayEffect";

	UPROPERTY(EditAnywhere, Category = "UAnimNotify_PlayEffect", DisplayName = "备注")
		FString HelpDesc;

	///绑定光效ID【配置表：DT_EffectCfg】
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "UAnimNotify_PlayEffect", DisplayName = "EffectID")
		FString EffectID = "";

private:
	int32 EffectUID = 0;
};

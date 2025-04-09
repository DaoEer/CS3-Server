// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimNotifies/AnimNotifyState.h"
#include "CS3AnimNotifyState.generated.h"

/*
 * 文件名称：CS3AnimNotifyState.h
 * 功能说明：CS3动画通知状态基类
 * 文件作者：huting
 * 目前维护：huting
 * 创建时间：2019-09-25
 */
UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "UCS3AnimNotifyState"))
class CHUANGSHI_API UCS3AnimNotifyState: public UAnimNotifyState
{
	GENERATED_UCLASS_BODY()

public:
	virtual void NotifyBegin(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation, float TotalDuration)override;

	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation);

	UFUNCTION(BlueprintImplementableEvent)
		bool Received_StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation) const;

public:
	bool bStopNotifyEffect = false;
};

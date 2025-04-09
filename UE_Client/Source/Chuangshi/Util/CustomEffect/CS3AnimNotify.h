// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimNotifies/AnimNotify.h"
#include "Util/CS3Debug.h"
#include "CS3AnimNotify.generated.h"

/*
 * 文件名称：CS3AnimNotify.h
 * 功能说明：CS3动画通知基类
 * 文件作者：huting
 * 目前维护：huting
 * 创建时间：2019-09-25
 */
UCLASS(Abstract, Blueprintable,const, hidecategories = Object, collapsecategories, meta = (DisplayName = "UCS3AnimNotify"))
class CHUANGSHI_API UCS3AnimNotify : public UAnimNotify
{
	GENERATED_BODY()

public:
	UCS3AnimNotify();

	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation);

	UFUNCTION(BlueprintImplementableEvent)
		bool Received_StopNotifyEffect(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation) const;
	
};

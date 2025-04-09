// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "StoryNotifyStateClear.generated.h"

/*
* 文件名称：StoryNotifyStateClear.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-05-22
*/

UCLASS(BlueprintType,meta = (DisplayName = "CS3StoryNotifyStateClear"))
class CHUANGSHI_API UStoryNotifyStateClear : public UCS3AnimNotifyState
{
	GENERATED_BODY()

		virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;

private:
	void ClearNotifyState(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation);
};

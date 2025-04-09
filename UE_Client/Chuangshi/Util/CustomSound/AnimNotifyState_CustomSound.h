// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "AnimNotifyState_CustomSound.generated.h"

/*
* 文件名称：AnimNotifyState_CustomSound.h
* 功能说明：自定义音效通知状态
* 文件作者：YangHan
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class ACustomSound;

UCLASS(abstract, meta = (DisplayName = "CS3AnimNotifyState_CustomSound"))
class CHUANGSHI_API UAnimNotifyState_CustomSound : public UCS3AnimNotifyState
{
	GENERATED_BODY()
	
public:
	UAnimNotifyState_CustomSound();

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;

	// Overridden from UAnimNotifyState to provide custom notify name.
	FString GetNotifyName_Implementation() const override;
	
public:
	// 自定义音效通知状态
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "UAnimNotifyState_CustomSound")
		FString NotifyType = "NotifyState_PlaySound";

	// 播放的音效（非循环音效无效,非循环音效请用Notify_PlaySound）
	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_CustomSound")
		USoundBase* Sound;

	// 音量因子（音量大小）
	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_CustomSound")
		float VolumeMultiplier;

	// 音高因子
	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_CustomSound")
		float PitchMultiplier;

	// 是否绑定
	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_CustomSound")
		bool bIsBind;

	// 绑定名字
	UPROPERTY(EditAnywhere, Category = "UAnimNotifyState_CustomSound")
		FName BindName;
private:
	UPROPERTY()
	TMap<USkeletalMeshComponent*, ACustomSound*>  CurSoundMap;
};

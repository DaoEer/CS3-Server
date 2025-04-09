// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Util/CustomEffect/CS3AnimNotify.h"
#include "AnimNotify_CustomSound.generated.h"

/*
* 文件名称：AnimNotify_CustomSound.h
* 功能说明：自定义音效通知
* 文件作者：YangHan
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class ACustomSound;
class USoundBase;

UCLASS(abstract, meta = (DisplayName = "CS3AnimNotify_CustomSound"))
class CHUANGSHI_API UAnimNotify_CustomSound : public UCS3AnimNotify
{
	GENERATED_BODY()
	
public:

	UAnimNotify_CustomSound();

	// Begin UAnimNotify interface
	virtual FString GetNotifyName_Implementation() const override;
	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	// End UAnimNotify interface
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
protected:
	void OnCurSoundFinish(ACustomSound* FinishSound);
public:
	// 自定义音效通知
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "UAnimNotify_CustomSound")
		FString NotifyType = "Notify_PlaySound";

	// 播放的音效(循环音效无效，循环音效请用NotifyState_PlaySound)
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		USoundBase* Sound;

	//音效开始的时间
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		float StartTime;

	// 音量因子（音量大小）
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		float VolumeMultiplier;

	// 音高因子
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		float PitchMultiplier;

	// 是否绑定
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		bool bIsBind;

	// 绑定名字
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_CustomSound")
		FName BindName;
private:
	UPROPERTY()
	TMap<USkeletalMeshComponent*, ACustomSound*>  CurSoundMap;
	
};

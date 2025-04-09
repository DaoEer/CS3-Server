// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotifyState.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimationAsset.h"
#include "SkeletalAnimParticle.h"
#include "AnimNotifyState_AttchSkeletalAnim.generated.h"

/*
 * 文件名称：UAnimNotifyState_AttchSkeletalAnim.h
 * 功能说明：绑定骨架网络物体到主角身上通知状态
 * 文件作者：ranyuan
 * 目前维护：ranyuan
 * 创建时间：2019-04-17
 */
UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotifyState_AttchSkeletalAnim"))
class CHUANGSHI_API UAnimNotifyState_AttchSkeletalAnim : public UCS3AnimNotifyState
{
	GENERATED_BODY()
public:
	UAnimNotifyState_AttchSkeletalAnim();

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)override;
public:

	///外挂骨骼动画（动画通知状态）
	///可以触发额外的骨骼动画表现
	///①表现循环播放，持续到相关通知状态注销时
	///②动画通知状态，跟随母动作中止
	///  ①若需要外挂动画不随母动画中止，应选用“动画通知”（BP_Notify_AttchSkeletalAnim）
	///注意：
	///①需要明确区分以下相似的通知
	///  ①BP_Notify_CS3SkeletalAnim
	///    ①专供“链刃甩链条表现”用
	///    ②详见CST - 4035，@冉渊
	///②BP_CS3AttachMeshPart
	///  ①主要由策划使用，依赖挂件配置（MeshBindID），重点在语境
	///  ②详见CST - 3883
	///③BP_Notify_AttchSkeletalAnim、BP_NotifyState_AttchSkeletalAnim
	///  ①主要由美术使用，依赖动画资源（Anim Asset），重点在表现
	///  ②详见CST - 7263	
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AnimNotify")
		FString NotifyName = "UAnimNotifyState_AttchSkeletalAnim";

	///插槽名字
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		FName SocketName;

	///是否绑定
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		uint32 Attached : 1;

	///位置偏移
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		FVector LocationOffset;

	///旋转偏移
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		FRotator RotationOffset;

	///缩放偏移
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim", DisplayName = "Scale3D Offset")
		FVector Scale3DOffset = FVector(1.0f);

	///骨架网格物体资源（留空视为没有表现）
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		USkeletalMesh* SkeletalMesh;

	///动画资源
	///	①配置留空时，视为“没有表现”
	///	②配置错误时，将会显示Tpose（如骨骼不一致）
	///	注意：
	///	①实际上无法排除“动画资源循环调用”的可能
	///	  ①策划同仁使用时应当保持谨慎，主动规避表现循环
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		UAnimationAsset* AnimAsset;

	///是否跟随母动作播放速度
	///	①True，默认，代表“动作速度是相对速度”
	///	  ①有效播放速度＝播放速度修正×子动作播放速度×母动作播放速度
	///	②False，代表“动作速度是绝对速度”
	///	  ①有效播放速度＝播放速度修正×子动作播放速度
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		bool AnimRateFollowParent = true;

	///播放速度修正（1.0代表“100%子动作播放速度”）
	UPROPERTY(EditAnywhere, Category = "UAnimNotify_AttchSkeletalAnim")
		float AnimRate = 1.0f;

	UPROPERTY()
	ASkeletalAnimParticle* SkeletalAnimPle;
};

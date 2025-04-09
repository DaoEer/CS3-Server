#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotify.h"
#include "Distributions/DistributionFloat.h"
#include "Engine/SkeletalMesh.h"
#include "Animation/AnimationAsset.h"
#include "Materials/MaterialInterface.h"
#include "Engine/Texture2D.h"
#include "ObjectMacros.h"
#include "SequencerAssistant.h"
#include "AnimNotify_CustomSkeletalAnim.generated.h"

/*
* 文件名称：AnimNotify_CustomSkeletalAnim.h
* 功能说明：为光效新添加一个骨骼动画 的动画消息
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-10-20
*/
class ASkeletalAnimParticle;

UCLASS(meta = (DisplayName = "CS3 Custom Skeletal Animation"))
class CHUANGSHI_API UAnimNotify_CustomSkeletalAnim : public UCS3AnimNotify
{
	GENERATED_UCLASS_BODY()

public:
	UAnimNotify_CustomSkeletalAnim();

	virtual void PostLoad() override;
#if WITH_EDITOR
	virtual void PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent) override;
#endif

	// End UObject interface

	// Begin UAnimNotify interface
	virtual FString GetNotifyName_Implementation() const override;

	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	// End UAnimNotify interface
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "AnimNotify")
		FString NotifyName = "CustomSkeletalAnimation";

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		USkeletalMesh* SkeletalMesh;

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		UAnimationAsset* AnimAsset;

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		UMaterialInterface* Material;

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		float MeshScale;

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		float AnimStartTime;
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		float AnimRate;
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		bool AnimRateFollowParent = true;

	//Should attach to the bone/socket
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		uint32 Attached : 1;

	// SocketName to attach to
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify", meta = (DisplayName = "SkeletalMesh bind to character's socket"))
		FName SocketName;

	// Location offset from the socket
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		FVector LocationOffset;

	// Rotation offset from socket
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		FRotator RotationOffset;

	//Break the particles when animation stop
	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify", meta = (DisplayName = ""))
		uint32 BreakWhenAnimStop : 1;

	UPROPERTY(EditAnywhere, Category = "SkeletalAnimNotify")
		uint32 IsWeapon : 1;

	//////////////////////////////////////////////////////////////////////////
	UPROPERTY(EditAnywhere, Category = "Particle")
		UParticleSystem* BindParticle;

	UPROPERTY(EditAnywhere, Category = "Particle", meta = (DisplayName = "Bind Particle bind to SkeletalMesh's socket"))
		FName BindParticleSokect;

	UPROPERTY(EditAnywhere, Category = "Fade")
		bool UseFadeInAndFadeOut;

	//控制Alpha，当UseFadeInAndFadeOut为True时有效
	UPROPERTY(EditAnywhere, Category = "Fade")
		FRawDistributionFloat AlphaControl;

	UPROPERTY(EditAnywhere, Category = "Dissolve")
		bool UseDissolve;

	// 同 AlphaControl，UseDissolve为True时有效
	UPROPERTY(EditAnywhere, Category = "Dissolve")
		FRawDistributionFloat DissolveControl;

	UPROPERTY(EditAnywhere, Category = "Dissolve")
		UTexture2D* DissolveTexture;
	UPROPERTY()
		class ASkeletalAnimParticle* SkelParticle;
};

// Fill out your copyright notice in the Description page of Project Settings.
/// 加载自定义的贴花粒子，粒子发射器的名字中含有"Decal"，会以贴花的方式加载，解决粒子切地的问题，zxm，2016年8月4日08:30:09
#pragma once

#include "CS3AnimNotify.h"
#include "Animation/AnimNotifies/AnimNotify_PlayParticleEffect.h"
#include "Particles/ParticleSystem.h"
#include "AnimNotify_CustomParticleEffect.generated.h"

/*
* 文件名称：AnimNotify_CustomParticleEffect.h
* 功能说明：
* 文件作者：zhengxuemei
* 目前维护：zhangfudong
* 创建时间：2016-10-20
*/

UCLASS(const, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3Custom Decal Particle Effect"))
class CHUANGSHI_API UAnimNotify_CustomParticleEffect: public UCS3AnimNotify
{
	GENERATED_BODY()
	
public:
	UAnimNotify_CustomParticleEffect();

	virtual void PostLoad() override;
#if WITH_EDITOR
	virtual void PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent) override;
#endif
	virtual void BeginDestroy() override;

	// End UObject interface

	// Begin UAnimNotify interface
	virtual FString GetNotifyName_Implementation() const override;

	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
	// End UAnimNotify interface
	
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;

	/// Particle System to Spawn
	UPROPERTY(EditAnywhere, Category = "AnimNotify", meta = (DisplayName = "Decal Particle System"))
		UParticleSystem* PSTemplate;

	/// Location offset from the socket
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		FVector LocationOffset;

	/// Rotation offset from socket
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		FRotator RotationOffset;

private:
	/// Cached version of the Rotation Offset already in Quat form
	FQuat RotationOffsetQuat;
				
	void _ParticleSysToDecals(USkeletalMeshComponent* MeshComp);
	
public:

	 ///Should attach to the bone/socket
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		uint32 Attached : 1; 	//~ Does not follow coding standard due to redirection from BP

								// SocketName to attach to
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		FName SocketName;
	//UPROPERTY()
	UParticleSystemComponent* PSC;
};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "Util/CS3Debug.h"
#include "CS3AnimNotify.h"
#include "CS3ParitcleAnimNotify.generated.h"


class UAnimSequenceBase;
class UParticleSystem;
class USkeletalMeshComponent;
class UParticleSystemComponent;
/*
 * 文件名称：CS3ParitcleAnimNotify.h
 * 功能说明：CS3光效动画通知基类
 * 文件作者：yaodi
 */
UCLASS(Abstract, Blueprintable, const, hidecategories = Object, collapsecategories, meta = (DisplayName = "UCS3ParitcleAnimNotify"))
class CHUANGSHI_API UCS3ParitcleAnimNotify : public UCS3AnimNotify
{
	GENERATED_BODY()

public:
	UCS3ParitcleAnimNotify();

	virtual void SetParNotifyRate(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation, float SeqRate);

	UFUNCTION(BlueprintImplementableEvent)
		bool Received_SetParNotifySacle(USkeletalMeshComponent * MeshComp, UAnimSequenceBase * Animation, float SeqRate) const;

	// Begin UObject interface
	virtual void PostLoad() override;
#if WITH_EDITOR
	virtual void PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent) override;
#endif
	// End UObject interface

	// Begin UAnimNotify interface
	virtual FString GetNotifyName_Implementation() const override;
	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;
#if WITH_EDITOR
	virtual void ValidateAssociatedAssets() override;


	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)override;

#endif
	// End UAnimNotify interface

	// Particle System to Spawn
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify", meta = (DisplayName = "Particle System"))
		UParticleSystem* PSTemplate;

	// Location offset from the socket
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify")
		FVector LocationOffset;

	// Rotation offset from socket
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify")
		FRotator RotationOffset;

	// Scale to spawn the particle system at
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		FVector Scale;

	// 特效播放速率 （光效播放速度与来源动画的播放速度无关）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify")
		float EffectRate = 1;

private:
	// Cached version of the Rotation Offset already in Quat form
	FQuat RotationOffsetQuat;

protected:
	// Spawns the ParticleSystemComponent. Called from Notify.
	virtual UParticleSystemComponent* SpawnParticleSystem(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation);

public:

	// Should attach to the bone/socket
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify")
		uint32 Attached : 1; 	//~ Does not follow coding standard due to redirection from BP

		// SocketName to attach to
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "AnimNotify")
		FName SocketName;
	//UPROPERTY()
	UParticleSystemComponent* PSC;
};

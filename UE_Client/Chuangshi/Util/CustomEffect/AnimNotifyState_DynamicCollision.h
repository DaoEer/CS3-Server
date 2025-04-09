// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Util/CustomEffect/CS3AnimNotifyState.h"
#include "AnimNotifyState_DynamicCollision.generated.h"

/**
* 文件名称：AnimNotifyState_DynamicCollision.h
* 功能说明：动态碰撞
* 文件作者：chendongyong
* 目前维护：chendongyong
* 创建时间：2019-11-19
 */

UCLASS(meta = (DisplayName = "DynamicCollision"))
class CHUANGSHI_API UAnimNotifyState_DynamicCollision : public UCS3AnimNotifyState
{
	GENERATED_BODY()
	typedef UCS3AnimNotifyState Supper;
	
public:
	UAnimNotifyState_DynamicCollision();

	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;

	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation);

	UFUNCTION()
	virtual void OnEmitterCollisionBegin(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
	UFUNCTION()
	virtual void OnEmitterCollisionEnd(UPrimitiveComponent* OverlappedComp, AActor* Other, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

#if WITH_EDITOR
	virtual void PreEditChange(UProperty* PropertyAboutToChange) override;
#endif

private:
	void _CalculateBox();

public:
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig", meta = (ToolTip = "Define Box high"))
		float BoxHigh;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig", meta = (ToolTip = "Define Box wide"))
		float BoxWide;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		float PerGrow;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		float GrowTime;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		float HoldTime;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		float PerDecay;
	/// Location offset from the socket
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		FVector BoxLocationOffset;
	/// Rotation offset from socket
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | BoxConfig")
		FRotator BoxRotationOffset;

	/// Particle System to Spawn
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		UParticleSystem* PSTemplate;

	/// Location offset from the socket
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		FVector LocationOffset;

	/// Rotation offset from socket
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		FRotator RotationOffset;

	// Should attach to the bone/socket
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Anim_Notify")
		uint32 Attached : 1; 	//~ Does not follow coding standard due to redirection from BP

	// SocketName to attach to
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		FName SocketName;
	//UPROPERTY()
	UParticleSystemComponent* PSC;

	// Whether or not we destroy the component at the end of the notify or instead just stop
	// the emitters.
	UPROPERTY(EditAnywhere, Category = Effect, meta = (DisplayName = "Destroy Immediately", ToolTip = "Whether the particle system should be immediately destroyed at the end of the notify state or be allowed to finish"))
		bool bDestroyAtEnd;

	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		int32 EnterSkillID;
	UPROPERTY(EditAnywhere, Category = "Anim_Notify | Effect")
		int32 LeaveSkillID;

private:
	class UBoxComponent* BoxCollision;
	float CurTime;


};

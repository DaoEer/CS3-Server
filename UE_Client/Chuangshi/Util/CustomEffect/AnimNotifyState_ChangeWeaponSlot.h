// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "CS3AnimNotifyState.h"
#include "ObjectMacros.h"
#include "AnimNotifyState_ChangeWeaponSlot.generated.h"

/*
* 文件名称：UAnimNotifyState_ChangeWeaponSlot.h
* 功能说明：切换武器插槽（主要应用于剑客拿剑左右手切换）
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-06-15
*/
UCLASS(const, Blueprintable, Abstract, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3AnimNotifyState_ChangeWeaponSlot"))
class CHUANGSHI_API UAnimNotifyState_ChangeWeaponSlot : public UCS3AnimNotifyState
{
	GENERATED_UCLASS_BODY()
public:
	virtual void NotifyBegin(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float TotalDuration) override;
	virtual void NotifyTick(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation, float FrameDeltaTime) override;
	virtual void NotifyEnd(class USkeletalMeshComponent * MeshComp, class UAnimSequenceBase * Animation) override;
	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation)override;
private:

public:

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "NotifyStateChangeWeaponSlot")
		FString NotifyType = "NotifyStateChangeWeaponSlot";

	UPROPERTY(EditAnywhere, Category = "NotifyStateChangeWeaponSlot", DisplayName = "备注")
		FString HelpDesc;

	///职业
	UPROPERTY(EditAnywhere, Category = "NotifyStateChangeWeaponSlot", DisplayName = "RoleProfession")
		int32 RoleProfession = 2;

	///性别
	UPROPERTY(EditAnywhere, Category = "NotifyStateChangeWeaponSlot", DisplayName = "RoleGender")
		int32 RoleGender = 1;
	
};

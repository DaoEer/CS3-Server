// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "../GameCharacter.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Component/Role/LadderCustomMovementComponent.h"
#include "BaseSubAnimInstance.generated.h"

/*
* 文件名称：BaseSubAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2020-02-21
*/
UCLASS()
class CHUANGSHI_API UBaseSubAnimInstance : public UAnimInstance
{
	GENERATED_BODY()
public:
	UBaseSubAnimInstance();
	~UBaseSubAnimInstance();
	void PostInitProperties() override;
	void NativeInitializeAnimation() override;
	void NativeUpdateAnimation(float DeltaSeconds) override;

protected:

private:

public:

protected:
	UPROPERTY(BlueprintReadOnly, Category = "BaseSubAnimInstance")
		AGameCharacter* CurCharacter;///当前角色

	UPROPERTY(BlueprintReadOnly, Category = "BaseSubAnimInstance")
		UCharacterMovementComponent* CurCharacterMovement;///当前角色移动组件 

	UPROPERTY(BlueprintReadOnly, Category = "BaseSubAnimInstance")
		ULadderCustomMovementComponent* LadderCustomMovementCpt;///当前角色梯子自定义的组件

	UPROPERTY(BlueprintReadOnly, Category = "BaseSubAnimInstance")
		UAnimSequence* ASLadderUpLoop;///攀爬梯子动作

	UPROPERTY(BlueprintReadWrite, Category = "BaseSubAnimInstance")
		float LadderPos;///当前角色自定义的组件

	UPROPERTY(BlueprintReadWrite, Category = "BaseSubAnimInstance")
		bool IsLadderModel;///当前角色自定义的组件

	UPROPERTY(BlueprintReadWrite, Category = "BaseSubAnimInstance")
		float LadderModelBlendTime;///当前角色自定义的组件
	
private:

};

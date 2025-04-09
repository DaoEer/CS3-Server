// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "HeadBaseAnimInstance.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UHeadBaseAnimInstance : public UAnimInstance
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		UAnimSequenceBase* CurAnimSquenceBase;

	///播放速率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		float PlayRate = 1.0f;

	///播放起始位置
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		float StartPosition = 0.0f;

	///是否循环
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "CharacterDataCode")
		bool bLoop = true;
};

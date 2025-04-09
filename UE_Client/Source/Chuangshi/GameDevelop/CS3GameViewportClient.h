// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameViewportClient.h"
#include "CS3GameViewportClient.generated.h"

/*
	重要度类型
*/
UENUM(BlueprintType)
enum class SignificanceType : uint8
{
	// 完整效果
	Complete,
	// 可以丢弃一些不太明显的效果
	Near,
	// 可以丢弃一些明显的效果
	Defect,
	// 可以只保留重要功能
	Bald,
	// 可以只保留核心功能
	Incomplete,
};

/**
 *  CS3GameViewportClient
 */
UCLASS()
class CHUANGSHI_API UCS3GameViewportClient : public UGameViewportClient
{
	GENERATED_BODY()
public:
	virtual void Tick(float DeltaTime) override;

	virtual void Init(FWorldContext& WorldContext, UGameInstance* OwningGameInstance, bool bCreateNewAudioDevice) override;
	//每帧更新的摄像机投影矩形
	FMatrix ProjMatrix;
};

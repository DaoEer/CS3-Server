// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Camera/CameraComponent.h"
#include "Engine/EngineTypes.h"
#include "Components/DirectionalLightComponent.h"
#include "CS3CameraComponent.generated.h"

/**
 * 
 */
UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class CHUANGSHI_API UCS3CameraComponent : public UCameraComponent
{
	GENERATED_BODY()
	
public:
	UCS3CameraComponent();///<构造函数
	virtual void BeginPlay() override;///<重写BeginPlay
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;///<重写EndPlay
};

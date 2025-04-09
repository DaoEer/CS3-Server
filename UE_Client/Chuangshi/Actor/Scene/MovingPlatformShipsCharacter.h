// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/Scene/MovingPlatformCharacter.h"
#include "Component/CS3CameraComponent.h"
#include "MovingPlatformShipsCharacter.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API AMovingPlatformShipsCharacter : public AMovingPlatformCharacter
{
	GENERATED_BODY()
public:
	AMovingPlatformShipsCharacter();///<构造函数
	virtual void BeginPlay()override;
		UPROPERTY(EditAnywhere, BlueprintReadWrite)
		class USpringArmComponentEX* SpringArmCompent;///<镜头摇臂

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UCS3CameraComponent* CameraComponent;///<镜头组件
};

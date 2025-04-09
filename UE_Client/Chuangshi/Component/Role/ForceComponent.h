// Fill out your copyright notice in the Description page of Project Settings.UForceComponent

#pragma once

#include "Components/SceneComponent.h"
#include "ForceComponent.generated.h"


/*
* 文件名称：ForceComponent.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-10-09
*/

UENUM(BlueprintType)
enum class ELOCAL_FORCE_DIRE : uint8
{
	None = 0,
	UP_DIRE = 1,
	DOWN_DIRE = 2,
	LIFT_DIRE = 3,
	RIGHT_DIRE = 4,
	FORWARD_DIRE = 5,
	BACK_DIRE = 6,
	LOOKAT_DIRE = 7
};

UCLASS(BlueprintType)
class CHUANGSHI_API UForceComponent : public USceneComponent
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	UForceComponent();

	/**
	*开始力
	*
	*@param _ForceSpeed 力的速度
	*@param _ForceDirection 力的方向
	*
	*@return 无
	*/
	void BeginForce(float _ForceSpeed,FVector _ForceDirection);
	void BeginForce(float _ForceSpeed, ELOCAL_FORCE_DIRE LocalDire);
	void StopForce();
	FVector& GetDirection() { return ForceDirection; }
	float GetSpeed() { return ForceSpeed; }
public:
	UPROPERTY()
	class UCapsuleComponent* CapsuleComponent;

protected:
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

public:
	float ForcePercentage;

protected:
	int ForceID;
	bool IsForceCanMove;
	float ForceSpeed;
	FVector ForceDirection;
	ELOCAL_FORCE_DIRE CurLocalDire;
};


// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "GameFramework/Pawn.h"
#include "WindComponent.generated.h"

/*
* 文件名称：WindComponent.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-09-23
*/

UCLASS(BlueprintType)
class CHUANGSHI_API AWindComponent : public APawn
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AWindComponent();

/**
*开始吹风
*
*@param _WindSpeed 风速
*@param _WindDirection 风的方向
*
*@return 无
*/
void BeginWind(float _WindSpeed,FVector _WindDirection);
void StopWind();

public:
	UPROPERTY()
	class UCapsuleComponent* CapsuleComponent;

protected:
	// Called every frame
	virtual void Tick(float DeltaTime) override;

private:
	bool IsWindCanMove;
	float WindSpeed;
	FVector WindDirection;
	
};

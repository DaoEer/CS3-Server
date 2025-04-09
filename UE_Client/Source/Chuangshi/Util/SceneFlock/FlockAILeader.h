// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/Actor.h"
#include "FlockAILeader.generated.h"

/*
* 文件名称：FlockAILeader.h
* 功能说明：
* 文件作者：jiangyupeng
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class USplineComponent;

UCLASS(BlueprintType)
class CHUANGSHI_API AFlockAILeader : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AFlockAILeader();

	bool bIsMove;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	
	
};

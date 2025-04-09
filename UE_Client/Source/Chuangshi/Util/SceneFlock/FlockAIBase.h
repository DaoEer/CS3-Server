// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameFramework/Actor.h"
#include "FlockAIBase.generated.h"

/*
* 文件名称：FlockAIBase.h
* 功能说明：
* 文件作者：jiangyupeng
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class AFlockAILeader;
class AFlockAISpawner;
class USphereComponent;
class USkeletalMeshComponent;
class UArrowComponent;
class APlayerCameraManager;
class AFlockAISpawner;
class UAnimSequence;

UCLASS(BlueprintType)
class CHUANGSHI_API AFlockAIBase : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AFlockAIBase();
	
	UPROPERTY(VisibleDefaultsOnly, Category = "Flock")
	USceneComponent* SceneRoot;

	UPROPERTY(VisibleDefaultsOnly, Category = "Flock")
	USphereComponent* CheckSphere;

	UPROPERTY(VisibleDefaultsOnly, Category = "Flock")
	USkeletalMeshComponent* FlockAIBody;

	UPROPERTY(VisibleDefaultsOnly, Category = "Flock")
	UArrowComponent* FlockBase;

public:

	// 权重
	float SeparationWeight;
	float EnemyWeight;
	float MoveToWeight;

	float MaxMovementSpeed;
	float BaseMovementSpeed;
	float MeetEnemyMovementSpeed;
	float BaseTurnSpeed;
	float MeetEnemyTurnSpeed;

	float TickIntervalBias;
	float FlockNum;
	float RoundSpeed;
	float DistBehindSpeedUpRange;

	UAnimSequence* AnimFly;
	UAnimSequence* AnimLand;
	UAnimSequence* AnimRandom;

	AFlockAILeader* MyFlockAILeader;

protected:

	static const UClass* AFlockAIBaseUClass;
	static const UClass* AFlockAIEnemyUClass;

	FVector CurrentFlockAILocation;		// 当前鱼和玩家摄像机的距离
	float CurrentMovementSpeed;
	FVector SpecificNeighbourLocation;	// 和某条具体的鱼的距离
	TSet<AActor*> Neighbourhood;

	AFlockAISpawner *MyFlockAISpawner;
	APlayerCameraManager *CurrentPlayerCameraMgr;

	FVector VectorCharCameraToFlockAI;
	float VectorSizeCharCameraToFlockAI;
	float TempDotProduct;

	bool bIsHasEnemy;
	bool bIsTooFar;

	FVector SeparationDistance;
	FVector MoveToDistance;
	FVector EnemyDistance;

	// 重置分离、移动和敌人的距离
	void ResetDistance();

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	void TurnRound(float DeltaTime);

	void RandMove(float DeltaTime);

private:

	bool bIsRandom;				// 原地转的方向
	bool bIsMove;				// 头鱼是否移动
	bool bIsReset;				// 状态重置
	bool bIsNearFlockLeaderl;	// 鱼是否靠近了头鱼
	FVector InitLocation;		// 鱼的初始位置
	FVector Distance;			// 和头鱼的距离
	FVector LastLocation;		// 上一帧的位置
	FVector MoveDirection;		// 鱼相对头鱼的位置
	float Radius;				// 头鱼不动的时候鱼游动半径	
	float RandSpeed;			// 随机速度的百分比
	float RandMoveDist;			// 鱼相对头鱼的位置的比例
	float RandMoveTime;			// 随机移动的时间
	float LimitTime;			// 时间的边界值
	float RandScale;			// 随机的比例

public:	

	virtual void Tick(float DeltaTime) override;

	void SetFlockAICheckCharCameraComp();

	void SetFlockAISpawner(AFlockAISpawner* Spawner);

	void SetFlockNum(float Num);

	void SetAnimSequence(UAnimSequence* FlySequence, UAnimSequence* LandSequence, UAnimSequence* RandomSequence);

	void SetSpeed(float Speed);

	bool SetFlockAILeader(AFlockAILeader* Leader);

protected:
	virtual void ProcessMoveEvent(const float DeltaTime);

	virtual void CalcMoveToDistance();

	virtual void CalcMoveSpeed(const float DeltaTime);
	
	virtual void UpdateTickInterval();

};

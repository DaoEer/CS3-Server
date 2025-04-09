// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Util/SceneFlock/FlockAILeader.h"
#include "FlockAISpawner.generated.h"

/*
* 文件名称：FlockAISpawner.h
* 功能说明：
* 文件作者：jiangyupeng
* 目前维护：wuxiaoou
* 创建时间：2017-10-18
*/

class AFlockAIBase;
class USplineComponent;
class USkeletalMesh;

UCLASS(BlueprintType)
class CHUANGSHI_API AFlockAISpawner : public AActor
{
	GENERATED_BODY()
	
public:

	AFlockAISpawner();

	UPROPERTY(VisibleDefaultsOnly, Category = "FlockLeader")
	USceneComponent* SceneRoot;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	TSubclassOf<AFlockAIBase> FlockAIType;


	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	AFlockAILeader* FlockLeader;

//	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	AFlockAIBase* FlockAI;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	int FlockAIAmount;
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	FVector SpawnScale;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	float MaxMovementSpeed;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	float RoundSpeed;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	float SpawnMaxRange;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	float SpawnMinRange;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	USkeletalMesh* SKMesh;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	UAnimSequence* AnimFly;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	UAnimSequence* AnimLand;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flock|Spawner")
	UAnimSequence* AnimRandom;



	// 存活时间，默认永远存活
	float FlockAILifeSpan;

	// 多久生成完
	float SpawnDuration;


	///////////////////////////////
	// 头鱼
	/////////////////////////////
	UPROPERTY(VisibleDefaultsOnly, Category = "Flock|FlockLeader")
	USplineComponent* SplineComp;

	UPROPERTY(EditAnywhere, Category = "Flock|FlockLeader")
	float Speed;						// 头鱼速度

	float CurrentScale;					// 当前头鱼已经走的长度与Spline总体长度的比例
	float SpeedScale;					// 速度和长度的比例，以此来决定一次多多长

public:	

	float SpawnRangeMaxX;
	float SpawnRangeMaxY;
	float SpawnRangeMaxZ;

	float SpawnRangeMinX;
	float SpawnRangeMinY;
	float SpawnRangeMinZ;

	FTransform SpawnTrans;
	uint32 CurrentFlockAICount;

	FTimerHandle SpawnFlockAITimeHandle;
	
	void LoopSpawn();

	void DoSpawnFlockAI();

	virtual void Tick(float DeltaTime) override;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	

	UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = "Flock|Spawner")
	void SpawnFlockAI();
	
};

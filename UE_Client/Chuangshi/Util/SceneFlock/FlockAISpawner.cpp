// Fill out your copyright notice in the Description page of Project Settings.


#include "FlockAISpawner.h"
#include "Util/SceneFlock/FlockAIBase.h"
#include "Components/SplineComponent.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameDevelop/CS3GameInstance.h"


// Sets default values
AFlockAISpawner::AFlockAISpawner()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;

	SplineComp = CreateDefaultSubobject<USplineComponent>(TEXT("SplineComp"));
	SplineComp->SetupAttachment(SceneRoot);
	SplineComp->SetClosedLoop(true);

	SpawnRangeMaxX = 0.f;
	SpawnRangeMaxY = 0.f;
	SpawnRangeMaxZ = 0.f;

	SpawnRangeMinX = 0.f;
	SpawnRangeMinY = 0.f;
	SpawnRangeMinZ = 0.f;

	SpawnMaxRange = 200;
	SpawnMinRange = -200;

	CurrentFlockAICount = 0;

	SKMesh = nullptr;
	AnimFly = nullptr;
	AnimLand = nullptr;
	AnimRandom = nullptr;
	RoundSpeed = 25.f;

	MaxMovementSpeed = 600.0f;
	Speed = MaxMovementSpeed - 100.0f;

	SpawnDuration = 5.f;
	SpawnScale = FVector(1.0f, 1.0f, 1.0f);
}

// Called when the game starts or when spawned
void AFlockAISpawner::BeginPlay()
{
	Super::BeginPlay();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}
	SpawnFlockAI();
	if (SplineComp->GetNumberOfSplinePoints() > 2)
	{
		FlockLeader->bIsMove = true;
	}
}


void AFlockAISpawner:: SpawnFlockAI_Implementation()
{
	if (FlockAIAmount > 0 && FlockAIType)
	{
		SpawnRangeMaxX = GetActorLocation().X + SpawnMaxRange;
		SpawnRangeMaxY = GetActorLocation().Y + SpawnMaxRange;
		SpawnRangeMaxZ = GetActorLocation().Z + SpawnMaxRange;

		SpawnRangeMinX = GetActorLocation().X + SpawnMinRange;
		SpawnRangeMinY = GetActorLocation().Y + SpawnMinRange;
		SpawnRangeMinZ = GetActorLocation().Z + SpawnMinRange;

		if (SpawnDuration > 1)
		{
			GetWorldTimerManager().SetTimer(SpawnFlockAITimeHandle, this, &AFlockAISpawner::LoopSpawn, SpawnDuration / FlockAIAmount, true);
		}
		else
		{
			for (int i = 0; i < FlockAIAmount; i++)
			{
				DoSpawnFlockAI();
			}
		}
	}

	else
	{
		GEngine->AddOnScreenDebugMessage(-1, 3.f, FColor::Red, FString("Warning!! A BP_Spawner FlockAIType is EMPTY OR FlockAIAmount is invalid !"));
		UE_LOG(LogTemp, Warning, TEXT("Warning!! A BP_Spawner FlockAIType is EMPTY OR FlockAIAmount is invalid !"));
		return;
	}
}

void AFlockAISpawner::LoopSpawn()
{
	DoSpawnFlockAI();
	if (CurrentFlockAICount == FlockAIAmount)
	{
		GetWorldTimerManager().ClearTimer(SpawnFlockAITimeHandle);
	}
}

void AFlockAISpawner::DoSpawnFlockAI()
{
	SpawnTrans = FTransform(FRotator(0.f, 0.f, 0.f), FVector(FMath::FRandRange(SpawnRangeMinX, SpawnRangeMaxX), FMath::FRandRange(SpawnRangeMinY, SpawnRangeMaxY), FMath::FRandRange(SpawnRangeMinZ, SpawnRangeMaxZ)),SpawnScale);

	AFlockAIBase* Flock = Cast<AFlockAIBase>(UGameplayStatics::BeginDeferredActorSpawnFromClass(this, FlockAIType, SpawnTrans));
// 	FActorSpawnParameters SpawnParams;
// 	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
// 	AFlockAIBase *Flock = Cast<AFlockAIBase>(GetWorld()->SpawnActor<AFlockAIBase>(AFlockAIBase::StaticClass(), SpawnTrans, SpawnParams));
	if (Flock)
	{
		Flock->SetLifeSpan(FlockAILifeSpan);
		Flock->SetFlockAISpawner(this);
		Flock->SetFlockNum(CurrentFlockAICount);
		Flock->FlockAIBody->SetSkeletalMesh(SKMesh);
		Flock->SetSpeed(RoundSpeed);
		Flock->SetAnimSequence(AnimFly, AnimLand, AnimRandom);
		Flock->SetFlockAILeader(FlockLeader);

		UGameplayStatics::FinishSpawningActor(Flock, SpawnTrans);
		++CurrentFlockAICount;
	}
}

void AFlockAISpawner::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	
	if (FlockLeader)
	{
		if (FlockLeader->bIsMove)
		{
			SpeedScale = Speed / SplineComp->GetSplineLength() * DeltaTime;
			FVector LeaderLocation = SplineComp->GetLocationAtDistanceAlongSpline(CurrentScale * SplineComp->GetSplineLength(), ESplineCoordinateSpace::World);
			FlockLeader->SetActorLocation(LeaderLocation);
			if (CurrentScale > 1.f)
				CurrentScale = 0.0f;
			else
				CurrentScale += SpeedScale;
		}
	}
}

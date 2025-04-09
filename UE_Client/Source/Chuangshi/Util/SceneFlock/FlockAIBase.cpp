// Fill out your copyright notice in the Description page of Project Settings.


#include "FlockAIBase.h"
#include "FlockAISpawner.h"
#include "FlockAILeader.h"
#include "Kismet/KismetMathLibrary.h"
#include "LandscapeStreamingProxy.h"
#include "Components/SphereComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/ArrowComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Animation/AnimSequence.h"
#include "GameFramework/Character.h"
#include "Components/StaticMeshComponent.h"

//const UClass* AFlockAIBase::AFlockAIBaseUClass = AFlockAIBase::StaticClass();


// Sets default values
AFlockAIBase::AFlockAIBase()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	RootComponent = SceneRoot;
	SceneRoot->SetComponentTickEnabled(false);

	CheckSphere = CreateDefaultSubobject<USphereComponent>(TEXT("FlockAICheckSphere"));
	CheckSphere->SetupAttachment(SceneRoot);
	CheckSphere->SetSphereRadius(30.0f);

	FlockAIBody = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("FlockAIBody"));
	FlockAIBody->SetupAttachment(SceneRoot);
	FlockAIBody->CastShadow = false;
	FlockAIBody->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	FlockAIBody->SetComponentTickEnabled(false);

	FlockBase = CreateDefaultSubobject<UArrowComponent>(TEXT("FlockBase"));
	FlockBase->AttachToComponent(RootComponent, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
	FlockBase->SetComponentTickEnabled(false);

	MyFlockAISpawner = nullptr;
	TickIntervalBias = 0.12f;

	// 每帧会更新的值
	VectorCharCameraToFlockAI = FVector(0.f, 0.f, 0.f);
	VectorSizeCharCameraToFlockAI = 0.f;
	TempDotProduct = 0.f;

	// 默认配置
	SeparationWeight = 200.f;
	EnemyWeight = 1400.f;
	MaxMovementSpeed = 600.f;
	BaseMovementSpeed = 150.f;
	MeetEnemyMovementSpeed = MaxMovementSpeed + 600.f;
	BaseTurnSpeed = 1.f;
	MeetEnemyTurnSpeed = 10.f;
	MoveToWeight = 5.f;

	CurrentMovementSpeed = 0.f;
	CurrentFlockAILocation = FVector(0.f, 0.f, 0.f);
	SpecificNeighbourLocation = FVector(0.f, 0.f, 0.f);

	SeparationDistance = FVector(0, 0, 0);
	EnemyDistance = FVector(0, 0, 0);
	MoveToDistance = FVector(0, 0, 0);

	RoundSpeed = 25.0f;
	AnimFly = nullptr;
	AnimLand = nullptr;
	AnimRandom = nullptr;

	MyFlockAILeader = nullptr;
	DistBehindSpeedUpRange = 300.0f;
	RandMoveDist = 200.0f;
	bIsRandom = false;
	bIsMove = false;
	bIsReset = true;

	bIsHasEnemy = false;
}

void AFlockAIBase::ResetDistance()
{
	CurrentFlockAILocation = GetActorLocation();
	SeparationDistance = FVector(0, 0, 0);
	EnemyDistance = FVector(0, 0, 0);
	MoveToDistance = FVector(0, 0, 0);
	bIsHasEnemy = false;
}

// Called when the game starts or when spawned
void AFlockAIBase::BeginPlay()
{
	Super::BeginPlay();
	SetFlockAICheckCharCameraComp();
	FlockAIBody->SetWorldRotation(FRotator(0, -90, 0));
	DistBehindSpeedUpRange = FMath::FRandRange(500.0f, 1700.0f);
	InitLocation = GetActorLocation();
}


void AFlockAIBase::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (SetFlockAILeader(MyFlockAILeader))
	{
		UpdateTickInterval();
		if (bIsTooFar)
		{
			if (MyFlockAILeader->bIsMove)
			{
				if (bIsReset)
				{
					//SetEllipseRotation();
					MoveDirection = FMath::VRand();
					RandMoveDist = FMath::FRandRange(-200, 200);
					LimitTime = FMath::FRandRange(3.0f, 6.0f);
					RandScale = FMath::FRandRange(20.0f, 50.0f);
					bIsReset = false;
				}
				RandMove(DeltaTime);
			}
			else
			{
				TurnRound(DeltaTime);
				if (bIsReset && bIsNearFlockLeaderl)
					bIsReset = false;
			}

		}
		else
		{
			bIsReset = true;
			RandMoveTime = 0.0f;
			ProcessMoveEvent(DeltaTime);
		}
	}
}


void AFlockAIBase::TurnRound(float DeltaTime)
{
	CheckSphere->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	CheckSphere->SetComponentTickEnabled(false);
	FlockAIBody->SetComponentTickEnabled(false);

	bIsNearFlockLeaderl = (GetActorLocation() == InitLocation);

	if (!bIsNearFlockLeaderl)
	{
		ResetDistance();
		CalcMoveToDistance();
		CalcMoveSpeed(DeltaTime);
		SetActorRotation(FMath::RInterpTo(GetActorRotation(),
			UKismetMathLibrary::FindLookAtRotation(GetActorLocation(), InitLocation),
			DeltaTime,
			BaseTurnSpeed));
		AddActorWorldOffset(GetActorForwardVector() * DeltaTime * CurrentMovementSpeed);
	}

	if (bIsReset && bIsNearFlockLeaderl)
	{
		Distance = GetActorLocation() - MyFlockAILeader->GetActorLocation();
		bIsRandom = FMath::RandBool();
		Radius = FMath::Sqrt(Distance.X * Distance.Y + Distance.Y * Distance.Y);
		RandSpeed = FMath::FRandRange(0.5f, 1.5f);
		LastLocation = FVector(0.0f, 0.0f, 0.0f);
	}

	// 绕圆转
	if (GetWorld() && bIsNearFlockLeaderl)
	{
		// 随机转一边
		if (bIsRandom)
		{
			float TempX = FMath::Sin(PI / (180.f) * (GetWorld()->GetTimeSeconds() * RoundSpeed * RandSpeed)) * Radius;
			float TempY = FMath::Cos(PI / (180.f) * (GetWorld()->GetTimeSeconds() * RoundSpeed * RandSpeed)) * Radius;
			SetActorLocation(MyFlockAILeader->GetActorLocation() + FVector(TempX, TempY, InitLocation.Z));
			// 设置他的旋转朝向
			FRotator ActorRotator = UKismetMathLibrary::ComposeRotators(UKismetMathLibrary::MakeRotFromX(GetActorLocation() - LastLocation), FRotator(0.0f, 0.0f, 0.0f));
			LastLocation = GetActorLocation();
			SetActorRotation(ActorRotator);
		}
		else
		{
			//SetActorRotation(FRotator(0.0f, -90.0f, 0.0f));
			float TempX = FMath::Sin(PI / (180.f) * (GetWorld()->GetTimeSeconds() * RoundSpeed * (-1) * RandSpeed)) * Radius;
			float TempY = FMath::Cos(PI / (180.f) * (GetWorld()->GetTimeSeconds() * RoundSpeed * (-1) * RandSpeed)) * Radius;
			SetActorLocation(MyFlockAILeader->GetActorLocation() + FVector(TempX, TempY, InitLocation.Z));
			// 设置他的旋转朝向
			FRotator ActorRotator = UKismetMathLibrary::ComposeRotators(UKismetMathLibrary::MakeRotFromX(GetActorLocation() - LastLocation), FRotator(0.0f, 0.0f, 0.0f));
			LastLocation = GetActorLocation();
			SetActorRotation(ActorRotator);
		}

	}
}

void AFlockAIBase::RandMove(float DeltaTime)
{
	CheckSphere->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	CheckSphere->SetComponentTickEnabled(false);
	FlockAIBody->SetComponentTickEnabled(false);
	if (!bIsReset)
	{
		ResetDistance();
		CalcMoveToDistance();
		CalcMoveSpeed(DeltaTime);
		SetActorRotation(UKismetMathLibrary::FindLookAtRotation(GetActorLocation(), MyFlockAILeader->GetActorLocation()));
		RandMoveTime += DeltaTime;

		if (RandMoveTime <= LimitTime)
		{
			bIsReset = false;
			float TempValue = FMath::Cos(PI / (180.f) * (GetWorld()->GetTimeSeconds() * RandScale));
			FVector TempLoc = (GetActorForwardVector() * DeltaTime * CurrentMovementSpeed) + (RandMoveDist * MoveDirection * TempValue * DeltaTime);
			AddActorWorldOffset(TempLoc);
		}
		else
		{
			RandMoveTime = 0.0f;
			bIsReset = true;
		}
	}
}

void AFlockAIBase::SetFlockAICheckCharCameraComp()
{
	CurrentPlayerCameraMgr = UGameplayStatics::GetPlayerCameraManager(this, 0);
}

void AFlockAIBase::SetFlockAISpawner(AFlockAISpawner* Spawner)
{
	MyFlockAISpawner = Spawner;
}

void AFlockAIBase::SetFlockNum(float Num)
{
	FlockNum = Num;
}

void AFlockAIBase::SetAnimSequence(UAnimSequence* FlySequence, UAnimSequence* LandSequence, UAnimSequence* RandomSequence)
{
	AnimFly = FlySequence;
	AnimLand = LandSequence;
	AnimRandom = RandomSequence;
}

void AFlockAIBase::SetSpeed(float Speed)
{
	RoundSpeed = Speed;
}

bool AFlockAIBase::SetFlockAILeader(AFlockAILeader* Leader)
{
	if (!IsValid(MyFlockAILeader))
	{
		MyFlockAILeader = Leader;
		if (MyFlockAILeader) 
			return true;
		else return false;
	}
	return true;
}

void AFlockAIBase::ProcessMoveEvent(const float DeltaTime)
{
	ResetDistance();

	// 计算鱼之间的分离距离和与敌人的距离
	CheckSphere->GetOverlappingActors(Neighbourhood);
	for (auto &TempNeighbour : Neighbourhood)
	{
		SpecificNeighbourLocation = TempNeighbour->GetActorLocation();
		if (TempNeighbour->GetClass()->IsChildOf(ACharacter::StaticClass()) || TempNeighbour->GetComponentByClass(UStaticMeshComponent::StaticClass()) || TempNeighbour->GetClass()->IsChildOf(ALandscapeStreamingProxy::StaticClass()))
		{
			ResetDistance();
			EnemyDistance = CurrentFlockAILocation - SpecificNeighbourLocation;
			bIsHasEnemy = true;
			break;
		}
		if ( TempNeighbour->GetClass()->IsChildOf(AFlockAIBase::StaticClass()))
		{
			if (TempNeighbour != this)
			{
				SeparationDistance += CurrentFlockAILocation - SpecificNeighbourLocation;
			}
		}
	}

	if (!bIsHasEnemy)
	{
		CalcMoveToDistance();
		CalcMoveSpeed(DeltaTime);
	}
	else
		CurrentMovementSpeed = MeetEnemyMovementSpeed;

	// 计算旋转
	SetActorRotation(FMath::RInterpTo(GetActorRotation(), 
									(SeparationDistance * SeparationWeight + EnemyDistance * EnemyWeight + MoveToDistance * MoveToWeight).ToOrientationRotator(), 
									DeltaTime, 
									(bIsHasEnemy ? MeetEnemyTurnSpeed : BaseTurnSpeed)));
	AddActorWorldOffset(GetActorForwardVector() * DeltaTime * CurrentMovementSpeed);
}

void AFlockAIBase::CalcMoveToDistance()
{
	// 计算移动的向量
	MoveToDistance = (MyFlockAILeader->GetActorLocation() - CurrentFlockAILocation);
}

void AFlockAIBase::CalcMoveSpeed(const float DeltaTime)
{
	// 根据距离来决定移动的速度
	if (GetDistanceTo(MyFlockAILeader) > DistBehindSpeedUpRange)
		CurrentMovementSpeed = CurrentMovementSpeed + DeltaTime * (MaxMovementSpeed - CurrentMovementSpeed);
	else
		CurrentMovementSpeed = CurrentMovementSpeed + DeltaTime * (BaseMovementSpeed - CurrentMovementSpeed);
}

void AFlockAIBase::UpdateTickInterval()
{
	VectorCharCameraToFlockAI = CurrentFlockAILocation - CurrentPlayerCameraMgr->GetCameraLocation();
	
	VectorSizeCharCameraToFlockAI = VectorCharCameraToFlockAI.Size();
	TempDotProduct = VectorCharCameraToFlockAI.GetSafeNormal() | FQuatRotationMatrix(CurrentPlayerCameraMgr->GetActorQuat()).GetUnitAxis(EAxis::X);

	if (VectorSizeCharCameraToFlockAI > 2000.f)
	{
		bIsTooFar = true;
		TickIntervalBias = 0.035f;
	}
	else
	{
		bIsTooFar = false;
		SceneRoot->SetComponentTickEnabled(true);
		CheckSphere->SetComponentTickEnabled(true);
		FlockAIBody->SetComponentTickEnabled(true);
		CheckSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		if (TempDotProduct >= 0.6f)
			PrimaryActorTick.TickInterval = 0.01f * FMath::Lerp(1.f, 3.f, VectorSizeCharCameraToFlockAI / 2000.f);
		else
			PrimaryActorTick.TickInterval = VectorSizeCharCameraToFlockAI < 500 ? 0.03f : 0.05f;
	}
}

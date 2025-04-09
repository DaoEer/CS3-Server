// Fill out your copyright notice in the Description page of Project Settings.


#include "Flock.h"
#include "Components/PoseableMeshComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CustomTimerManager.h"
#include "Components/ArrowComponent.h"
#include "Manager/CustomTimerManager.h"

// Sets default values
AFlock::AFlock()
{
	PrimaryActorTick.bCanEverTick = true;
	DefaultSceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("SceneRoot"));
	Mesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("MainSkeletalMesh"));
	FlockBase = CreateDefaultSubobject<UArrowComponent>(TEXT("FlockBase"));
	FlockBase->AttachToComponent(DefaultSceneRoot, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
	Mesh->AttachToComponent(FlockBase, FAttachmentTransformRules(EAttachmentRule::KeepRelative, false));
	FlockTickInterval = 0.03f;
	Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	PrimaryActorTick.TickInterval = 0.03f; 
}

// Called when the game starts or when spawned
void AFlock::BeginPlay()
{
	Super::BeginPlay();
	if (IsValid(UUECS3GameInstance::Instance))
	{
		OnEndPlay.AddUniqueDynamic(UUECS3GameInstance::Instance, &UUECS3GameInstance::OnActorEndPlay);
	}
	GetCharCamera();

	Mesh->SetSkeletalMesh(SKMesh);
	Mesh->SetWorldRotation(FRotator(0,-90,0));
	
	Fly();
	CenterPosition = DefaultSceneRoot->RelativeLocation;
	if(IsFly)
		CenterPosition += FVector(FMath::FRandRange(0, Offset.X), FMath::FRandRange(0, Offset.Y), FMath::FRandRange(0, Offset.Z));

	Speed = FlySpeed;

	EllipseA = MaxCubeRange.X + FMath::RandRange(0 - MaxCubeRange.X * 0.2f, MaxCubeRange.X * 0.2f);
	EllipseB = MaxCubeRange.Y + FMath::RandRange(0 - MaxCubeRange.Y * 0.2f, MaxCubeRange.Y * 0.2f);

	// 计算椭圆轨迹作为XY坐标
	CurrPlaneAngle = (Index * DistanceInterval + InitialPos) * 3.1415f / 180.f;
	FVector2D EllipsePoint = GetEllipseLocation(CurrPlaneAngle, EllipseA, EllipseB);
	// 计算Z坐标
	CurrZAngle = IsFly ? Index * DistanceInterval * 3.1415f / 180.f : 0.f;
	float OffsetZ = FMath::Sin(CurrZAngle) * MaxCubeRange.Z;
	FVector NewPosition = CenterPosition + FVector(EllipsePoint.X, EllipsePoint.Y, OffsetZ);
	FlockBase->SetWorldLocation(NewPosition);
	Mesh->SetComponentTickEnabled(false);
	//Mesh->SetVisibility(false, true);
	//Mesh->Stop(); 
	//GEngine->AddOnScreenDebugMessage(-1, 10.0f, FColor::Red, "Test Print"); 
}

// Called every frame
void AFlock::Tick( float DeltaTime )
{
	Super::Tick(DeltaTime);
	 
	UpdateTickInterval();
	MoveEvent();

} 

void AFlock::Destroyed()
{
}

bool AFlock::ShouldTickIfViewportsOnly() const
{
	return true;
}

FVector2D AFlock::GetEllipseLocation(float Angle, float A, float B)
{
	return FVector2D(FMath::Cos(Angle) * A, FMath::Sin(Angle) * B);
}

float AFlock::GetEllipsePointSlope(float x, float y, float A, float B, float Theta)
{
	float slope = -(x * B * B) / (y * A * A);
	float angle = FMath::Atan(slope) * 180.f / 3.1415f;

 	if (Theta > 0 && Theta < 3.1415f)
 		angle += 180.0f;

	return angle;
}

void AFlock::MakeAngleInRange(float& Angle)
{
	if (Angle >= 3.1415f)
	{
		Angle -= 3.1415f * 2.f;
		MakeAngleInRange(Angle);
	}
	else if (Angle < -3.1415f)
	{
		Angle += 3.1415f * 2.f;
		MakeAngleInRange(Angle);
	}
}

void AFlock::GetEllipseTangentPoint(float x, float y, float A, float B)
{
	float T = FMath::Asin(1 - FMath::Sqrt(FMath::Square(y / B) + FMath::Square(x / A)));
	float Beta = FMath::Atan(B / A); // 2个值
	float Theta = T - Beta;

}

void AFlock::MoveEvent()
{
	if (IsFly)
	{
		if (!Mesh->IsPlaying())
			Mesh->PlayAnimation(AnimFly, true);

		CurrPlaneAngle += Speed * FlockTickInterval;
		MakeAngleInRange(CurrPlaneAngle);
		FVector2D EllipsePoint = GetEllipseLocation(CurrPlaneAngle, EllipseA, EllipseB);
		CurrZAngle += UpSpeed * FlockTickInterval;
		float OffsetZ = FMath::Sin(CurrZAngle) * MaxCubeRange.Z;
		FVector NewPosition = CenterPosition + FVector(EllipsePoint.X, EllipsePoint.Y, OffsetZ);
		FlockBase->SetWorldLocation(NewPosition);
		float SlopeAnle = GetEllipsePointSlope(EllipsePoint.X, EllipsePoint.Y, EllipseA, EllipseB, CurrPlaneAngle);
		//FlockBase->SetWorldLocationAndRotation(NewPosition, FRotator(0, 0, SlopeAnle));
		FlockBase->SetWorldRotation(FRotator(0, SlopeAnle, 0));
	}
	if (IsRandom)
	{
		if (!Mesh->IsPlaying())
			RestToFly();
	}
}

void AFlock::Fly()
{
	if (AnimFly)
	{
		IsFly = true;
		IsRandom = false;
		Mesh->PlayAnimation(AnimFly, true);
		Mesh->GlobalAnimRateScale = FMath::RandRange(0.85f, 1.15f);
		Speed = FlySpeed;
	}
	else
	{
		Land();
	}
}

void AFlock::Land()
{
	if (AnimLand)
	{
		LandTime = FMath::RandRange(LandTimeRange.X, LandTimeRange.Y);
		Mesh->PlayAnimation(AnimLand, true);
		FTimerHandle TimerHandle;
		TWeakObjectPtr<AFlock> DelayThisPtr(this);
		if (UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					AFlock* ThisPtr = DelayThisPtr.Get();
					ThisPtr->LandRandom();
				}
			}), LandTime / 2.f, false);
		}
		else
		{
			GetWorld()->GetTimerManager().SetTimer(TimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					AFlock* ThisPtr = DelayThisPtr.Get();
					ThisPtr->LandRandom();
				}
			}), LandTime / 2.f, false);
		}
	}
}

void AFlock::LandRandom()
{
	float RandomRate = FMath::RandRange(0, 100);
	if (RandomRate < 50 && AnimRandom)
	{
		IsRandom = true;
		Mesh->PlayAnimation(AnimRandom, false);
	}
	else
	{
		RestToFly();
	}
}

void AFlock::RestToFly()
{
	if (AnimLand)
		Mesh->PlayAnimation(AnimLand, true);
	FTimerHandle TimerHandle;
	TWeakObjectPtr<AFlock> DelayThisPtr(this);
	if (UUECS3GameInstance::Instance)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, TimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				AFlock* ThisPtr = DelayThisPtr.Get();
				ThisPtr->Fly();
			}
		}), LandTime / 2.f, false);
	}
	else
	{
		GetWorld()->GetTimerManager().SetTimer(TimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				AFlock* ThisPtr = DelayThisPtr.Get();
				ThisPtr->Fly();
			}
		}), LandTime / 2.f, false);
	}
}

void AFlock::GetCharCamera()
{
	 CurrentPlayerCamera = UGameplayStatics::GetPlayerCameraManager(this, 0);
}

void AFlock::UpdateTickInterval()
{
	FlockToCharacter = GetActorLocation() - CurrentPlayerCamera->GetCameraLocation();
	float FlockToCharacterSize = FlockToCharacter.Size();
	
	// 通过点积来计算他们之间的夹角
	//float TmpDotProduct = FlockToCharacter.GetSafeNormal() | FQuatRotationMatrix(CurrentPlayerCamera->GetActorQuat()).GetUnitAxis(EAxis::X);
	
 	if (FlockToCharacterSize > DistanceToHide)
 	{
		Mesh->SetComponentTickEnabled(false);

 	}
 	else
 	{
		Mesh->SetComponentTickEnabled(true);
 	}
} 

